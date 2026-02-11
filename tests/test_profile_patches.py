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

        self.assertIn('position_lat', field_names)
        self.assertIn('position_long', field_names)
        self.assertIn('date', field_names)
        self.assertIn('count', field_names)
        self.assertIn('clock_time', field_names)

    def test_patched_location_message_field_types(self):
        location = MESSAGE_TYPES[29]

        position_lat = location.fields[1]
        self.assertEqual(position_lat.name, 'position_lat')
        self.assertEqual(position_lat.units, 'semicircles')

        date_field = location.fields[8]
        self.assertEqual(date_field.name, 'date')


if __name__ == '__main__':
    unittest.main()
