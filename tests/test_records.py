#!/usr/bin/env python

from fitparse.profile import MESSAGE_TYPES
from fitparse.records import Crc, FieldData

import unittest

class RecordsTestCase(unittest.TestCase):
    def test_field_data_takes_positional_arguments_in_slot_order(self):
        heart_rate = MESSAGE_TYPES[20].fields[3]
        field_data = FieldData(None, heart_rate, None, 150, 150)
        self.assertEqual(
            (field_data.field_def, field_data.field, field_data.parent_field,
             field_data.value, field_data.raw_value, field_data.units),
            (None, heart_rate, None, 150, 150, 'bpm'),
        )

    def test_field_data_keeps_explicit_units(self):
        heart_rate = MESSAGE_TYPES[20].fields[3]
        self.assertEqual(FieldData(field=heart_rate, value=2.5, units='Hz').units, 'Hz')

    def test_crc(self):
        crc = Crc()
        self.assertEqual(0, crc.value)
        crc.update(b'\x0e\x10\x98\x00(\x00\x00\x00.FIT')
        self.assertEqual(0xace7, crc.value)
        # 0 must not change the crc
        crc.update(0)
        self.assertEqual(0xace7, crc.value)

    def test_crc_format(self):
        self.assertEqual('0x0000', Crc.format(0))
        self.assertEqual('0x12AB', Crc.format(0x12AB))


if __name__ == '__main__':
    unittest.main()
