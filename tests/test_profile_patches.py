#!/usr/bin/env python

import unittest
from fitparse.profile import MESSAGE_TYPES, FIELD_TYPES


class ProfilePatchesTestCase(unittest.TestCase):
    def test_patched_message_types_present(self):
        self.assertIn(29, MESSAGE_TYPES)
        self.assertEqual(MESSAGE_TYPES[29].name, 'location')

    def test_patched_location_message_fields(self):
        location = MESSAGE_TYPES[29]
        field_names = {f.name for f in location.fields.values()}

        self.assertEqual(
            field_names,
            {'name', 'position_lat', 'position_long', 'altitude', 'message_index'},
        )
        self.assertNotIn(3, location.fields)
        self.assertNotIn(8, location.fields)

    def test_patched_location_message_field_types(self):
        location = MESSAGE_TYPES[29]

        position_lat = location.fields[1]
        self.assertEqual(position_lat.name, 'position_lat')
        self.assertEqual(position_lat.units, 'semicircles')

        name = location.fields[0]
        self.assertEqual(name.name, 'name')
        self.assertEqual(name.type.name, 'string')

        altitude = location.fields[4]
        self.assertEqual(altitude.name, 'altitude')
        self.assertEqual((altitude.scale, altitude.offset, altitude.units), (5, 500, 'm'))

        message_index = location.fields[254]
        self.assertEqual(message_index.name, 'message_index')
        self.assertIs(message_index.type, FIELD_TYPES['message_index'])

    def test_patched_stress_level_body_battery_field(self):
        stress_level = MESSAGE_TYPES[227]
        field_names = {f.name for f in stress_level.fields.values()}

        self.assertIn('stress_level_value', field_names)
        self.assertIn('stress_level_time', field_names)

        body_battery = stress_level.fields[3]
        self.assertEqual(body_battery.name, 'body_battery')
        self.assertEqual(body_battery.units, 'percent')


if __name__ == '__main__':
    unittest.main()
