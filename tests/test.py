#!/usr/bin/env python

import csv
import datetime
import os
import random
from struct import pack
import warnings

from fitparse import FitFile
from fitparse.processors import UTC_REFERENCE, StandardUnitsDataProcessor
from fitparse.records import BASE_TYPES, Crc
from fitparse.utils import FitEOFError, FitCRCError, FitHeaderError, FitParseError

import unittest


def generate_messages(mesg_num, local_mesg_num, field_defs, endian='<', data=None):
    mesgs = []
    base_type_list = []

    # definition message, local message num
    s = pack('<B', 0x40 | local_mesg_num)
    # reserved byte and endian
    s += pack('<xB', int(endian == '>'))
    # global message num, num fields
    s += pack('%sHB' % endian, mesg_num, len(field_defs))
    for def_num, base_type in field_defs:
        base_type = [bt for bt in BASE_TYPES.values() if bt.name == base_type][0]
        base_type_list.append(base_type)
        s += pack('<3B', def_num, base_type.size, base_type.identifier)

    mesgs.append(s)

    if data:
        for mesg_data in data:
            s = pack('B', local_mesg_num)
            for value, base_type in zip(mesg_data, base_type_list):
                s += pack("{}{}".format(endian, base_type.fmt), value)
            mesgs.append(s)

    return b''.join(mesgs)


def generate_fitfile(data=None, endian='<'):
    fit_data = (
        generate_messages(
            # local mesg 0, global mesg 0 (file_id)
            mesg_num=0, local_mesg_num=0, endian=endian, field_defs=[
                # serial number, time_created, manufacturer
                (3, 'uint32z'), (4, 'uint32'), (1, 'uint16'),
                # product/garmin_product, number, type
                (2, 'uint16'), (5, 'uint16'), (0, 'enum'),
            ],
            # random serial number, random time, garmin, edge500, null, activity
            data=[[558069241, 723842606, 1, 1036, (2 ** 16) - 1, 4]],
        )
    )

    if data:
        fit_data += data

    # Prototcol version 1.0, profile version 1.52
    header = pack('<2BHI4s', 14, 16, 152, len(fit_data), b'.FIT')
    file_data = header + pack('<' + Crc.FMT, Crc.calculate(header)) + fit_data
    return file_data + pack('<' + Crc.FMT, Crc.calculate(file_data))


def raw_definition(mesg_num, local_mesg_num, field_defs):
    s = pack('<BxBHB', 0x40 | local_mesg_num, 0, mesg_num, len(field_defs))
    for def_num, size, base_type_id in field_defs:
        s += pack('<3B', def_num, size, base_type_id)
    return s


def raw_data(local_mesg_num, payload):
    return pack('B', local_mesg_num) + payload


RECORD_SIZE = 6


def records_fitfile(count, trailer=b''):
    data = raw_definition(20, 1, [(253, 4, 0x86), (3, 1, 0x02)])
    for n in range(count):
        data += raw_data(1, pack('<IB', 723842606 + n, 120 + n))
    return generate_fitfile(data + trailer)


def dev_record_fitfile(description_fields, description_payload, dev_value):
    data = (
        raw_definition(207, 1, [(3, 1, 0x02)]) + raw_data(1, b'\x00')
        + raw_definition(206, 2, [(0, 1, 0x02), (1, 1, 0x02), (2, 1, 0x02), (3, 4, 0x07)]
                         + description_fields)
        + raw_data(2, b'\x00\x00\x84pwr\x00' + description_payload)
        + pack('<BxBHB', 0x60 | 3, 0, 20, 1) + pack('<3B', 253, 4, 0x86) + pack('<B3B', 1, 0, 2, 0)
        + raw_data(3, pack('<IH', 723842606, dev_value))
    )
    return generate_fitfile(data)


def corrupt(data, rng):
    body = bytearray(data[:-2])
    for _ in range(rng.randint(1, 4)):
        body[rng.randrange(body[0], len(body))] = rng.randrange(256)
    return bytes(body) + pack('<' + Crc.FMT, Crc.calculate(bytes(body)))


def secs_to_dt(secs):
    return datetime.datetime.fromtimestamp(timestamp=(secs + UTC_REFERENCE), tz=datetime.timezone.utc).replace(tzinfo=None)


def testfile(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', filename)


class FitFileTestCase(unittest.TestCase):

    def test_basic_file_with_one_record(self, endian='<'):
        f = FitFile(generate_fitfile(endian=endian))
        f.parse()

        self.assertEqual(f.profile_version, 1.52)
        self.assertEqual(f.protocol_version, 1.0)

        file_id = f.messages[0]
        self.assertEqual(file_id.name, 'file_id')

        for field in ('type', 0):
            self.assertEqual(file_id.get_value(field), 'activity')
            self.assertEqual(file_id.get(field).raw_value, 4)
        for field in ('manufacturer', 1):
            self.assertEqual(file_id.get_value(field), 'garmin')
            self.assertEqual(file_id.get(field).raw_value, 1)
        for field in ('product', 'garmin_product', 2):
            self.assertEqual(file_id.get_value(field), 'edge500')
            self.assertEqual(file_id.get(field).raw_value, 1036)
        for field in ('serial_number', 3):
            self.assertEqual(file_id.get_value(field), 558069241)
        for field in ('time_created', 4):
            self.assertEqual(file_id.get_value(field), secs_to_dt(723842606))
            self.assertEqual(file_id.get(field).raw_value, 723842606)
        for field in ('number', 5):
            self.assertEqual(file_id.get_value(field), None)

    def test_basic_file_big_endian(self):
        self.test_basic_file_with_one_record('>')

    def test_component_field_accumulaters(self):
        # TODO: abstract CSV parsing
        csv_fp = open(testfile('compressed-speed-distance-records.csv'))
        csv_file = csv.reader(csv_fp)
        next(csv_file)  # Consume header

        f = FitFile(testfile('compressed-speed-distance.fit'))
        f.parse()

        records = f.get_messages(name='record')
        empty_record = next(records)  # Skip empty record for now (sets timestamp via header)

        # File's timestamp record is < 0x10000000, so field returns seconds
        self.assertEqual(empty_record.get_value('timestamp'), 17217864)

        # TODO: update using local_timestamp as offset, since we have this value as 2012 date

        for count, (record, (timestamp, heartrate, speed, distance, cadence)) in enumerate(zip(records, csv_file)):
            # No fancy datetime stuff, since timestamp record is < 0x10000000
            fit_ts = record.get_value('timestamp')
            self.assertIsInstance(fit_ts, int)
            self.assertLess(fit_ts, 0x10000000)
            self.assertEqual(fit_ts, int(timestamp))

            self.assertEqual(record.get_value('heart_rate'), int(heartrate))
            self.assertEqual(record.get_value('cadence'), int(cadence) if cadence != 'null' else None)
            self.assertAlmostEqual(record.get_value('speed'), float(speed))
            self.assertAlmostEqual(record.get_value('distance'), float(distance))

        self.assertEqual(count, 753)  # TODO: confirm size(records) = size(csv)
        csv_fp.close()

    def test_accumulator_survives_a_redefinition(self):
        for second_local_mesg_num in (1, 2):
            with self.subTest(second_local_mesg_num=second_local_mesg_num):
                field_defs = [(253, 'uint32'), (18, 'uint8')]
                fit_data = generate_fitfile(
                    generate_messages(
                        mesg_num=20, local_mesg_num=1, field_defs=field_defs,
                        data=[[723842606, 250], [723842607, 4]],
                    )
                    + generate_messages(
                        mesg_num=20, local_mesg_num=second_local_mesg_num, field_defs=field_defs,
                        data=[[723842608, 10]],
                    )
                )

                f = FitFile(fit_data)
                totals = [m.get_value('total_cycles') for m in f.get_messages('record')]
                self.assertEqual(totals, [250, 260, 266])

    WALKING_INTENSITY = 6 | 3 << 5
    CYCLING_INTENSITY = 2 | 5 << 5

    def monitoring_messages(self, field_defs, data):
        fit_data = generate_fitfile(
            generate_messages(mesg_num=55, local_mesg_num=1, field_defs=field_defs, data=data)
        )
        return list(FitFile(fit_data).get_messages('monitoring'))

    def test_subfield_resolves_against_a_component_reference(self):
        orders = {
            'cycles first': ([(26, 'uint16'), (3, 'uint32'), (24, 'byte')], lambda c, a: [1000, c, a]),
            'cycles last': ([(26, 'uint16'), (24, 'byte'), (3, 'uint32')], lambda c, a: [1000, a, c]),
        }
        for order, (field_defs, row) in orders.items():
            with self.subTest(order=order):
                walking, cycling = self.monitoring_messages(
                    field_defs, [row(1739, self.WALKING_INTENSITY), row(420, self.CYCLING_INTENSITY)],
                )
                self.assertEqual(walking.get_value('activity_type'), 'walking')
                self.assertEqual(walking.get_value('steps'), 1739)
                self.assertNotIn('cycles', [fd.name for fd in walking.fields])
                self.assertEqual(cycling.get_value('activity_type'), 'cycling')
                self.assertEqual(cycling.get_value('strokes'), 210.0)
                self.assertNotIn('cycles', [fd.name for fd in cycling.fields])

    def test_native_reference_wins_over_a_component_reference(self):
        (message,) = self.monitoring_messages(
            [(5, 'enum'), (24, 'byte'), (3, 'uint32')], [[2, self.WALKING_INTENSITY, 420]],
        )
        self.assertEqual(message.get_value('strokes'), 210.0)
        self.assertIsNone(message.get_value('steps'))

    def test_invalid_native_reference_falls_back_to_a_component_reference(self):
        (message,) = self.monitoring_messages(
            [(5, 'enum'), (24, 'byte'), (3, 'uint32')], [[0xFF, self.WALKING_INTENSITY, 1739]],
        )
        self.assertEqual(message.get_value('steps'), 1739)

    def test_component_field_resolves_subfield(self):
        fit_data = generate_fitfile(
            generate_messages(
                # event (21), local message 1
                mesg_num=21, local_mesg_num=1, field_defs=[
                    # event, event_type, data16
                    (0, 'enum'), (1, 'enum'), (2, 'uint16'),
                ],
                data=[[0, 0, 2]],
            )
        )

        f = FitFile(fit_data)
        f.parse()

        event = f.messages[1]
        self.assertEqual(event.name, 'event')
        for field in ('event', 0):
            self.assertEqual(event.get_value(field), 'timer')
            self.assertEqual(event.get(field).raw_value, 0)
        for field in ('event_type', 1):
            self.assertEqual(event.get_value(field), 'start')
            self.assertEqual(event.get(field).raw_value, 0)

        # Should be able to reference by original field name,
        # component field name, subfield name, and then the field def_num of both
        # the original field and component field
        for field in ('timer_trigger', 'data', 3):
            self.assertEqual(event.get_value(field), 'fitness_equipment')
            self.assertEqual(event.get(field).raw_value, 2)

        # Component field should be left as is
        for field in ('data16', 2):
            self.assertEqual(event.get_value(field), 2)

    def test_subfield_components(self):
        # sore = 123, opponent_score = 456, total = 29884539
        sport_point_value = 123 + (456 << 16)
        # rear_gear_num = 4, rear_gear, = 20, front_gear_num = 2, front_gear = 34
        gear_chance_value = 4 + (20 << 8) + (2 << 16) + (34 << 24)

        fit_data = generate_fitfile(
            generate_messages(
                # event (21), local message 1
                mesg_num=21, local_mesg_num=1, field_defs=[
                    # event, data
                    (0, 'enum'), (3, 'uint32'),
                ],
                data=[
                    # sport point
                    [33, sport_point_value],
                    # front gear change
                    [42, gear_chance_value],
                ],
            )
        )

        f = FitFile(fit_data)
        f.parse()

        sport_point = f.messages[1]
        self.assertEqual(sport_point.name, 'event')
        for field in ('event', 0):
            self.assertEqual(sport_point.get_value(field), 'sport_point')
            self.assertEqual(sport_point.get(field).raw_value, 33)
        for field in ('sport_point', 'data', 3):
            # Verify raw numeric value
            self.assertEqual(sport_point.get_value(field), sport_point_value)
        for field in ('score', 7):
            self.assertEqual(sport_point.get_value(field), 123)
        for field in ('opponent_score', 8):
            self.assertEqual(sport_point.get_value(field), 456)

        gear_change = f.messages[2]
        self.assertEqual(gear_change.name, 'event')
        for field in ('event', 0):
            self.assertEqual(gear_change.get_value(field), 'front_gear_change')
            self.assertEqual(gear_change.get(field).raw_value, 42)
        for field in ('gear_change_data', 'data', 3):
            # Verify raw numeric value
            self.assertEqual(gear_change.get_value(field), gear_chance_value)
        for field in ('front_gear_num', 9):
            self.assertEqual(gear_change.get_value(field), 2)
        for field in ('front_gear', 10):
            self.assertEqual(gear_change.get_value(field), 34)
        for field in ('rear_gear_num', 11):
            self.assertEqual(gear_change.get_value(field), 4)
        for field in ('rear_gear', 12):
            self.assertEqual(gear_change.get_value(field), 20)

    def test_parsing_edge_500_fit_file(self):
        self._csv_test_helper(
            'garmin-edge-500-activity.fit',
            'garmin-edge-500-activity-records.csv')

    def test_parsing_fenix_5_bike_fit_file(self):
        self._csv_test_helper(
            'garmin-fenix-5-bike.fit',
            'garmin-fenix-5-bike-records.csv')

    def test_parsing_fenix_5_run_fit_file(self):
        self._csv_test_helper(
            'garmin-fenix-5-run.fit',
            'garmin-fenix-5-run-records.csv')

    def test_parsing_fenix_5_walk_fit_file(self):
        self._csv_test_helper(
            'garmin-fenix-5-walk.fit',
            'garmin-fenix-5-walk-records.csv')

    def test_parsing_edge_820_fit_file(self):
        self._csv_test_helper(
            'garmin-edge-820-bike.fit',
            'garmin-edge-820-bike-records.csv')

    def _csv_test_helper(self, fit_file, csv_file):
        csv_fp = open(testfile(csv_file))
        csv_messages = csv.reader(csv_fp)
        field_names = next(csv_messages)  # Consume header

        f = FitFile(testfile(fit_file))
        messages = f.get_messages(name='record')

        # For fixups
        last_valid_lat, last_valid_long = None, None

        for message, csv_message in zip(messages, csv_messages):
            for csv_index, field_name in enumerate(field_names):
                fit_value, csv_value = message.get_value(field_name), csv_message[csv_index]
                if field_name == 'timestamp':
                    # Adjust GMT to PDT and format
                    fit_value = (fit_value - datetime.timedelta(hours=7)).strftime("%a %b %d %H:%M:%S PDT %Y")

                # Track last valid lat/longs
                if field_name == 'position_lat':
                    if fit_value is not None:
                        last_valid_lat = fit_value
                if field_name == 'position_long':
                    if fit_value is not None:
                        last_valid_long = fit_value

                # ANT FIT SDK Dump tool does a bad job of logging invalids, so fix them
                if fit_value is None:
                    # ANT FIT SDK Dump tool cadence reports invalid as 0
                    if field_name == 'cadence' and csv_value == '0':
                        csv_value = None
                    # ANT FIT SDK Dump tool invalid lat/lng reports as last valid
                    if field_name == 'position_lat':
                        fit_value = last_valid_lat
                    if field_name == 'position_long':
                        fit_value = last_valid_long

                if isinstance(fit_value, int):
                    csv_value = int(fit_value)
                if csv_value == '':
                    csv_value = None

                if isinstance(fit_value, float):
                    # Float comparison
                    self.assertAlmostEqual(fit_value, float(csv_value))
                else:
                    self.assertEqual(fit_value, csv_value,
                        msg="For {}, FIT value '{}' did not match CSV value '{}'".format(field_name, fit_value, csv_value))

        try:
            next(messages)
            self.fail(".FIT file had more than csv file")
        except StopIteration:
            pass

        try:
            next(csv_messages)
            self.fail(".CSV file had more messages than .FIT file")
        except StopIteration:
            pass

        csv_fp.close()

    def test_developer_types(self):
        """Test that a file with developer types in it can be parsed"""
        FitFile(testfile('developer-types-sample.fit')).parse()
        FitFile(testfile('20170518-191602-1740899583.fit')).parse()
        FitFile(testfile('DeveloperData.fit')).parse()

    def test_invalid_crc(self):
        try:
            FitFile(testfile('activity-filecrc.fit')).parse()
            self.fail("Didn't detect an invalid CRC")
        except FitCRCError:
            pass

    def test_unexpected_eof(self):
        try:
            with warnings.catch_warnings(record=True):
                FitFile(testfile('activity-unexpected-eof.fit')).parse()
            self.fail("Didn't detect an unexpected EOF")
        except FitEOFError:
            pass

    def test_chained_file(self):
        FitFile(testfile('activity-settings.fit')).parse()

    def test_invalid_chained_files(self):
        """Detect errors when files are chained together

        Note that 'chained' means just concatinated in this case
        """
        try:
            FitFile(testfile('activity-activity-filecrc.fit')).parse()
            self.fail("Didn't detect a CRC error in the chained file")
        except FitCRCError:
            pass

        try:
            FitFile(testfile('activity-settings-corruptheader.fit')).parse()
            self.fail("Didn't detect a header error in the chained file")
        except FitHeaderError:
            pass

        try:
            FitFile(testfile('activity-settings-nodata.fit')).parse()
            self.fail("Didn't detect an EOF error in the chaned file")
        except FitEOFError:
            pass

    def test_valid_files(self):
        """Test that parsing a bunch of random known-good files works"""
        for x in ('2013-02-06-12-11-14.fit', '2015-10-13-08-43-15.fit',
                  'Activity.fit', 'Edge810-Vector-2013-08-16-15-35-10.fit',
                  'MonitoringFile.fit', 'Settings.fit', 'Settings2.fit',
                  'WeightScaleMultiUser.fit', 'WeightScaleSingleUser.fit',
                  'WorkoutCustomTargetValues.fit', 'WorkoutIndividualSteps.fit',
                  'WorkoutRepeatGreaterThanStep.fit', 'WorkoutRepeatSteps.fit',
                  'activity-large-fenxi2-multisport.fit', 'activity-small-fenix2-run.fit',
                  'antfs-dump.63.fit', 'sample-activity-indoor-trainer.fit',
                  'sample-activity.fit', 'garmin-fenix-5-bike.fit',
                  'garmin-fenix-5-run.fit', 'garmin-fenix-5-walk.fit',
                  'garmin-edge-820-bike.fit', 'null_compressed_speed_dist.fit'):
            FitFile(testfile(x)).parse()

    def test_units_processor(self):
        for x in ('2013-02-06-12-11-14.fit', '2015-10-13-08-43-15.fit',
                  'Activity.fit', 'Edge810-Vector-2013-08-16-15-35-10.fit',
                  'MonitoringFile.fit', 'Settings.fit', 'Settings2.fit',
                  'WeightScaleMultiUser.fit', 'WeightScaleSingleUser.fit',
                  'WorkoutCustomTargetValues.fit', 'WorkoutIndividualSteps.fit',
                  'WorkoutRepeatGreaterThanStep.fit', 'WorkoutRepeatSteps.fit',
                  'activity-large-fenxi2-multisport.fit', 'activity-small-fenix2-run.fit',
                  'antfs-dump.63.fit', 'sample-activity-indoor-trainer.fit',
                  'sample-activity.fit', 'garmin-fenix-5-bike.fit',
                  'garmin-fenix-5-run.fit', 'garmin-fenix-5-walk.fit',
                  'garmin-edge-820-bike.fit'):
            FitFile(testfile(x), data_processor=StandardUnitsDataProcessor()).parse()

    def test_int_long(self):
        """Test that ints are properly shifted and scaled"""
        with FitFile(testfile('event_timestamp.fit')) as f:
            assert f.messages[-1].fields[1].raw_value == 863.486328125

    def test_elemnt_bolt_developer_data_id_without_application_id(self):
        """Test that a file without application id set inside developer_data_id is parsed
        (as seen on ELEMNT BOLT with firmware version WB09-1507)"""
        FitFile(testfile('elemnt-bolt-no-application-id-inside-developer-data-id.fit')).parse()

    def test_multiple_header(self):
        f = FitFile(testfile('sample_mulitple_header.fit'))
        assert len(f.messages) == 3023

    def test_speed(self):
        f = FitFile(testfile('2019-02-17-062644-ELEMNT-297E-195-0.fit'))
        avg_speed = list(f.get_messages('session'))[0].get_values().get('avg_speed')
        self.assertEqual(avg_speed, 5.86)

    def test_mismatched_field_size(self):
        f = FitFile(testfile('coros-pace-2-cycling-misaligned-fields.fit'))
        with warnings.catch_warnings(record=True) as w:
            f.parse()
            assert w
            assert all(
                "falling back to byte encoding" in str(x)
                for x in w
                if x.category == UserWarning
            )
        self.assertEqual(len(f.messages), 11293)

    def test_unterminated_file(self):
        f = FitFile(testfile('nick.fit'), check_crc=False)
        with warnings.catch_warnings(record=True) as w:
            f.parse()

    def test_check_crc_false_parses_a_valid_file(self):
        data = generate_fitfile(raw_definition(20, 1, [(253, 4, 0x86)]) + raw_data(1, pack('<I', 723842606)))
        checked = FitFile(data)
        checked.parse()
        unchecked = FitFile(data, check_crc=False)
        unchecked.parse()
        self.assertEqual(
            [m.get_values() for m in unchecked.messages],
            [m.get_values() for m in checked.messages],
        )

    def test_check_crc_false_parses_a_file_with_a_wrong_crc(self):
        data = generate_fitfile()
        data = data[:-2] + pack('<' + Crc.FMT, Crc.calculate(data[:-2]) ^ 0xFFFF)
        with self.assertRaises(FitCRCError):
            FitFile(data).parse()
        f = FitFile(data, check_crc=False)
        f.parse()
        self.assertEqual(len(f.messages), 1)

        FitFile(testfile('activity-filecrc.fit'), check_crc=False).parse()

    def test_check_crc_false_reads_chained_files(self):
        checked = FitFile(testfile('activity-settings.fit'))
        checked.parse()
        unchecked = FitFile(testfile('activity-settings.fit'), check_crc=False)
        unchecked.parse()
        self.assertEqual(len(unchecked.messages), len(checked.messages))

    def test_check_crc_false_tolerates_a_missing_crc(self):
        f = FitFile(generate_fitfile()[:-2], check_crc=False)
        f.parse()
        self.assertEqual(len(f.messages), 1)

    def _values(self, fit):
        return [m.get_values() for m in fit.get_messages()]

    def _parse_truncated(self, data):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            f = FitFile(data, allow_truncated=True)
            f.parse()
        self.assertEqual([str(x.message) for x in w], [])
        return f

    def test_allow_truncated_keeps_a_complete_file_as_is(self):
        data = records_fitfile(3)
        f = self._parse_truncated(data)
        self.assertIsNone(f.truncated)
        self.assertEqual(self._values(f), self._values(FitFile(data)))

    def test_allow_truncated_keeps_every_message_before_a_cut_at_a_message_boundary(self):
        data = records_fitfile(3)
        f = self._parse_truncated(data[:-2 - RECORD_SIZE])
        self.assertIsInstance(f.truncated, FitEOFError)
        self.assertEqual(self._values(f), self._values(FitFile(data))[:-1])

    def test_allow_truncated_drops_the_message_the_cut_went_through(self):
        data = records_fitfile(3)
        f = self._parse_truncated(data[:-2 - RECORD_SIZE // 2])
        self.assertIsInstance(f.truncated, FitEOFError)
        self.assertEqual(self._values(f), self._values(FitFile(data))[:-1])

    def test_allow_truncated_keeps_every_message_before_a_cut_definition(self):
        data = records_fitfile(2, raw_definition(21, 2, [(253, 4, 0x86), (0, 1, 0x00)]))
        f = self._parse_truncated(data[:-2 - 4])
        self.assertIsInstance(f.truncated, FitEOFError)
        self.assertEqual(self._values(f), self._values(FitFile(data)))

    def test_allow_truncated_keeps_every_message_of_a_file_missing_its_crc(self):
        data = records_fitfile(3)
        f = self._parse_truncated(data[:-2])
        self.assertIsInstance(f.truncated, FitEOFError)
        self.assertEqual(self._values(f), self._values(FitFile(data)))

    def test_allow_truncated_still_raises_on_a_full_length_file_read_past_its_end(self):
        data = generate_fitfile(raw_definition(20, 1, [(253, 4, 0x86)]) + raw_data(1, b'\x00\x00'))
        with self.assertRaises(FitEOFError):
            FitFile(data, allow_truncated=True).parse()

    def test_allow_truncated_keeps_the_complete_segments_of_a_cut_chained_file(self):
        with open(testfile('activity-settings.fit'), 'rb') as fh:
            data = fh.read()
        first_segment = self._values(FitFile(data[:771]))
        for cut in (775, 800):
            f = self._parse_truncated(data[:cut])
            self.assertIsInstance(f.truncated, FitEOFError)
            self.assertEqual(self._values(f)[:len(first_segment)], first_segment)

    def test_allow_truncated_recovers_a_truncated_fixture(self):
        f = self._parse_truncated(testfile('activity-unexpected-eof.fit'))
        self.assertIsInstance(f.truncated, FitEOFError)
        self.assertTrue(f.messages)

    def test_developer_data_thread_safe(self):
        """
        Test that a file with developer types in it can be parsed thread-safe.
        This test opens 2 FIT files and tests whether the dev_types of one does not change the dev_types of the other.
        """
        fit_file_1 = FitFile(testfile('developer-types-sample.fit'))
        field_description_count = 0
        for message in fit_file_1.get_messages():
            if message.mesg_type.name == "field_description":
                field_description_count += 1
                if field_description_count >= 4:
                    # Break after final field description message
                    break

        fit_file_2 = FitFile(testfile('developer-types-sample.fit'))
        for message in fit_file_2.get_messages():
            if message.mesg_type.name == "developer_data_id":
                break

        try:
            fit_file_1.parse()
        except FitParseError:
            self.fail("parse() unexpectedly raised a FitParseError")


    def test_invalid_size_on_an_unknown_field_falls_back_to_bytes(self):
        data = raw_definition(20, 1, [(250, 3, 0x84)]) + raw_data(1, b'\x01\x02\x03')
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            f = FitFile(generate_fitfile(data))
            f.parse()
        assert any("'unknown_250'" in str(x.message) for x in w)
        self.assertEqual(f.messages[1].get(250).raw_value, (1, 2, 3))

    def test_array_valued_date_time_keeps_its_raw_values(self):
        data = raw_definition(0, 1, [(4, 8, 0x86)]) + raw_data(1, pack('<2I', 723842606, 723842607))
        f = FitFile(generate_fitfile(data))
        f.parse()
        self.assertEqual(f.messages[1].get_value('time_created'), (723842606, 723842607))

    def test_array_valued_timestamp_does_not_anchor_compressed_timestamps(self):
        data = (
            raw_definition(20, 1, [(253, 8, 0x86)])
            + raw_data(1, pack('<2I', 723842606, 723842607))
            + pack('B', 0x80 | (1 << 5) | 3) + pack('<2I', 1, 2)
        )
        f = FitFile(generate_fitfile(data))
        f.parse()
        self.assertEqual(len(f.messages), 3)

    def test_component_of_an_array_with_invalid_elements_is_none(self):
        data = raw_definition(20, 1, [(8, 3, 0x02)]) + raw_data(1, b'\x01\xff\x03')
        f = FitFile(generate_fitfile(data))
        f.parse()
        self.assertIsNone(f.messages[1].get_value('speed'))
        self.assertIsNone(f.messages[1].get_value('distance'))

    def test_dev_field_description_with_an_unknown_base_type_falls_back_to_bytes(self):
        data = (
            raw_definition(207, 1, [(3, 1, 0x02)]) + raw_data(1, b'\x00')
            + raw_definition(206, 2, [(0, 1, 0x02), (1, 1, 0x02), (2, 1, 0x02), (3, 4, 0x07)])
            + raw_data(2, b'\x00\x00\x99abc\x00')
        )
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            f = FitFile(generate_fitfile(data))
            f.parse()
        assert any('Unknown base type' in str(x.message) for x in w)
        dev_field = f.dev_types[0]['fields'][0]
        self.assertEqual(dev_field.type.name, 'byte')
        self.assertEqual(dev_field.name, 'abc')

    def test_dev_field_description_with_a_non_string_name_gets_a_placeholder(self):
        data = (
            raw_definition(207, 1, [(3, 1, 0x02)]) + raw_data(1, b'\x00')
            + raw_definition(206, 2, [(0, 1, 0x02), (1, 1, 0x02), (2, 1, 0x02), (3, 4, 0x02)])
            + raw_data(2, b'\x00\x05\x02abc\x00')
        )
        f = FitFile(generate_fitfile(data))
        f.parse()
        self.assertEqual(f.dev_types[0]['fields'][5].name, 'unnamed_dev_field_5')

    def _dev_record_field(self, data):
        f = FitFile(data)
        return next(f.get_messages('record')).get('pwr')

    def test_dev_field_applies_the_description_scale_and_offset(self):
        field_data = self._dev_record_field(dev_record_fitfile(
            [(6, 1, 0x02), (7, 1, 0x01)], pack('<Bb', 10, 5), 2000,
        ))
        self.assertEqual(field_data.raw_value, 2000)
        self.assertEqual(field_data.value, 195.0)

    def test_dev_field_without_scale_or_offset_keeps_its_raw_value(self):
        field_data = self._dev_record_field(dev_record_fitfile(
            [(6, 1, 0x02), (7, 1, 0x01)], pack('<Bb', 0xFF, 0x7F), 2000,
        ))
        self.assertEqual(field_data.value, 2000)

    def test_dev_field_exposes_its_native_message_and_field(self):
        field_data = self._dev_record_field(dev_record_fitfile(
            [(14, 2, 0x84), (15, 1, 0x02)], pack('<HB', 20, 7), 2000,
        ))
        self.assertEqual((field_data.field.native_mesg_num, field_data.field.native_field_num), (20, 7))
        self.assertEqual(field_data.value, 2000)

    def test_dev_field_description_with_an_array_index_raises_fit_parse_error(self):
        data = (
            raw_definition(207, 1, [(3, 1, 0x02)]) + raw_data(1, b'\x00')
            + raw_definition(206, 2, [(0, 2, 0x02), (1, 1, 0x02), (2, 1, 0x02)])
            + raw_data(2, b'\x00\x00\x00\x02')
        )
        with self.assertRaises(FitParseError):
            FitFile(generate_fitfile(data)).parse()

    def test_corrupted_files_only_raise_fit_parse_error(self):
        rng = random.Random(20261109)
        originals = [
            testfile(name) for name in (
                'Activity.fit', 'DeveloperData.fit', 'MonitoringFile.fit',
                'compressed-speed-distance.fit', 'Settings.fit', 'WorkoutIndividualSteps.fit',
            )
        ]
        for variant in range(150):
            with open(rng.choice(originals), 'rb') as fh:
                data = corrupt(fh.read(), rng)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                for allow_truncated in (False, True):
                    try:
                        FitFile(data, allow_truncated=allow_truncated).parse()
                    except FitParseError:
                        pass

    # TODO:
    #  * Test Processors:
    #    - process_type_<>, process_field_<>, process_units_<>, process_message_<>


if __name__ == '__main__':
    unittest.main()
