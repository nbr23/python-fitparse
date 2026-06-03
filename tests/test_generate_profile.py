#!/usr/bin/env python

import sys
import os
import unittest
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from generate_profile import (
    apply_patches,
    load_message_type_patches,
    load_field_type_patches,
    load_patches_from_directory,
    MessageInfo,
    MessageList,
    TypeInfo,
    TypeList,
    FieldInfo,
)


class GenerateProfileTestCase(unittest.TestCase):
    def test_load_message_type_patches(self):
        patches = load_message_type_patches()
        self.assertIn(29, patches)
        self.assertEqual(patches[29].name, 'location')
        self.assertIsInstance(patches[29], MessageInfo)

    def test_load_field_type_patches(self):
        patches = load_field_type_patches()
        self.assertIsInstance(patches, dict)

    def test_load_patches_from_nonexistent_directory(self):
        patches = load_patches_from_directory('/nonexistent/path', 'message_types')
        self.assertEqual(patches, {})

    def test_load_patches_invalid_type(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            patches = load_patches_from_directory(tmpdir, 'invalid_type')
            self.assertEqual(patches, {})

    def test_load_patches_missing_required_attributes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            patch_file = os.path.join(tmpdir, 'bad_patch.py')
            with open(patch_file, 'w') as f:
                f.write('# missing MESSAGE_INFO\n')

            patches = load_patches_from_directory(tmpdir, 'message_types')
            self.assertEqual(patches, {})

    def test_message_patch_structure(self):
        patches = load_message_type_patches()
        if 29 in patches:
            location = patches[29]
            self.assertEqual(location.num, 29)
            self.assertIsInstance(location.fields, list)
            self.assertGreater(len(location.fields), 0)

            for field in location.fields:
                self.assertIsInstance(field, FieldInfo)
                self.assertIsNotNone(field.name)
                self.assertIsNotNone(field.type)
                self.assertIsNotNone(field.num)


class MergeFieldsTestCase(unittest.TestCase):
    def _stress_level_stub(self):
        return MessageInfo(
            name='stress_level', num=227, group_name='', comment='',
            fields=[
                FieldInfo(name='stress_level_value', type='sint16', num=0,
                          scale=None, offset=None, units=None,
                          components=[], subfields=[], comment=''),
                FieldInfo(name='stress_level_time', type='date_time', num=1,
                          scale=None, offset=None, units='s',
                          components=[], subfields=[], comment=''),
            ],
        )

    def test_patch_merges_field_into_existing_message(self):
        message_list = MessageList([self._stress_level_stub()])
        apply_patches(TypeList([]), message_list)

        merged = next(m for m in message_list.messages if m.num == 227)
        by_num = {f.num: f for f in merged.fields}
        self.assertEqual(by_num[3].name, 'body_battery')
        self.assertEqual(by_num[3].units, 'percent')
        self.assertEqual(by_num[0].name, 'stress_level_value')
        self.assertEqual(by_num[1].name, 'stress_level_time')

    def test_patch_does_not_overwrite_existing_field(self):
        stub = self._stress_level_stub()
        stub.fields.append(FieldInfo(name='preexisting', type='sint8', num=3,
                                     scale=None, offset=None, units=None,
                                     components=[], subfields=[], comment=''))
        message_list = MessageList([stub])
        apply_patches(TypeList([]), message_list)

        merged = next(m for m in message_list.messages if m.num == 227)
        fields_at_3 = [f for f in merged.fields if f.num == 3]
        self.assertEqual(len(fields_at_3), 1)
        self.assertEqual(fields_at_3[0].name, 'preexisting')


if __name__ == '__main__':
    unittest.main()
