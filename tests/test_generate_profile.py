#!/usr/bin/env python

import sys
import os
import unittest
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from generate_profile import (
    load_message_type_patches,
    load_field_type_patches,
    load_patches_from_directory,
    MessageInfo,
    TypeInfo,
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


if __name__ == '__main__':
    unittest.main()
