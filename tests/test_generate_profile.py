#!/usr/bin/env python

import sys
import os
import unittest
import tempfile
import shutil
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from generate_profile import (
    apply_patches,
    load_message_type_patches,
    load_field_type_patches,
    load_patches_from_directory,
    resolve_references,
    ComponentFieldInfo,
    MessageInfo,
    MessageList,
    PatchError,
    ReferenceFieldInfo,
    SubFieldInfo,
    TypeInfo,
    TypeList,
    TypeValueInfo,
    FieldInfo,
)


def field(name, num, type='uint8', subfields=None, components=None):
    return FieldInfo(name=name, type=type, num=num, scale=None, offset=None, units=None,
                     components=components or [], subfields=subfields or [], comment='')


def message(name, num, fields):
    return MessageInfo(name=name, num=num, group_name='', fields=fields, comment='')


def type_info(name, values, base_type='enum'):
    return TypeInfo(name=name, base_type=base_type, comment='',
                    values=[TypeValueInfo(name=n, value=v, comment='') for v, n in values])


def subfield(name, num, ref_name, ref_value):
    return SubFieldInfo(name=name, num=num, type='uint8', scale=None, offset=None, units=None,
                        ref_fields=[ReferenceFieldInfo(name=ref_name, value=ref_value, num=None, raw_value=None)],
                        components=[], comment='')


def write_patch(directory, filename, body):
    with open(os.path.join(directory, filename), 'w') as f:
        f.write(body)


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
            with self.assertRaises(PatchError):
                load_patches_from_directory(tmpdir, 'invalid_type')

    def test_load_patches_missing_required_attributes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            write_patch(tmpdir, 'bad_patch.py', 'VALUE = 1\n')
            with self.assertRaises(PatchError):
                load_patches_from_directory(tmpdir, 'message_types')

    def test_load_patches_broken_file_is_fatal(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            write_patch(tmpdir, 'broken.py', 'MESSAGE_INFO = (\n')
            with self.assertRaises(SyntaxError):
                load_patches_from_directory(tmpdir, 'message_types')

    def test_load_patches_duplicate_key_is_fatal(self):
        body = (
            'from generate_profile import MessageInfo\n'
            "MESSAGE_INFO = MessageInfo(name='x', num=300, group_name='', fields=[], comment='')\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            write_patch(tmpdir, 'a.py', body)
            write_patch(tmpdir, 'b.py', body)
            with self.assertRaises(PatchError):
                load_patches_from_directory(tmpdir, 'message_types')

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

    def test_patch_conflicting_with_official_field_is_fatal(self):
        stub = self._stress_level_stub()
        stub.fields.append(field('preexisting', 3, type='sint8'))
        with self.assertRaises(PatchError):
            apply_patches(TypeList([]), MessageList([stub]))

    def test_patch_already_official_is_not_duplicated(self):
        stub = self._stress_level_stub()
        stub.fields.append(field('body_battery', 3, type='sint8'))
        message_list = MessageList([stub])
        apply_patches(TypeList([]), message_list)

        merged = next(m for m in message_list.messages if m.num == 227)
        self.assertEqual([f.name for f in merged.fields if f.num == 3], ['body_battery'])


class PatchSemanticsTestCase(unittest.TestCase):
    def _apply(self, type_list, message_list, message_patches=None, type_patches=None):
        with mock.patch('generate_profile.load_message_type_patches', return_value=message_patches or {}), \
                mock.patch('generate_profile.load_field_type_patches', return_value=type_patches or {}):
            return apply_patches(type_list, message_list)

    def test_message_num_with_another_official_name_is_fatal(self):
        official = MessageList([message('waypoint', 29, [field('label', 0)])])
        with self.assertRaises(PatchError):
            self._apply(TypeList([]), official, {29: message('location', 29, [field('name', 0)])})

    def test_same_name_field_gains_patched_subfields(self):
        official = MessageList([message('event', 21, [field('event', 0), field('data', 3)])])
        patch = message('event', 21, [field('data', 3, subfields=[subfield('new_alert', 3, 'event', 'new_event')])])
        applied = self._apply(TypeList([]), official, {21: patch})

        data = official.messages[0].get('data')
        self.assertEqual([s.name for s in data.subfields], ['new_alert'])
        self.assertEqual(applied, 1)

    def test_existing_subfield_is_not_duplicated(self):
        existing = subfield('alert', 3, 'event', 'alert_event')
        official = MessageList([message('event', 21, [field('event', 0), field('data', 3, subfields=[existing])])])
        patch = message('event', 21, [field('data', 3, subfields=[subfield('alert', 3, 'event', 'alert_event')])])
        self.assertEqual(self._apply(TypeList([]), official, {21: patch}), 0)
        self.assertEqual(len(official.messages[0].get('data').subfields), 1)

    def test_enum_value_is_added_to_an_existing_type(self):
        types = TypeList([type_info('event', [(0, 'timer')])])
        applied = self._apply(types, MessageList([]), type_patches={'event': type_info('event', [(99, 'new_event')])})

        self.assertEqual(applied, 1)
        self.assertEqual(types.get('event').get('new_event').value, 99)

    def test_enum_value_conflict_is_fatal(self):
        types = TypeList([type_info('event', [(0, 'timer')])])
        with self.assertRaises(PatchError):
            self._apply(types, MessageList([]), type_patches={'event': type_info('event', [(0, 'stopwatch')])})

    def test_redundant_enum_value_is_not_duplicated(self):
        types = TypeList([type_info('event', [(0, 'timer')])])
        self.assertEqual(self._apply(types, MessageList([]), type_patches={'event': type_info('event', [(0, 'timer')])}), 0)
        self.assertEqual(len(types.get('event').values), 1)

    def test_enum_base_type_mismatch_is_fatal(self):
        types = TypeList([type_info('event', [(0, 'timer')])])
        with self.assertRaises(PatchError):
            self._apply(types, MessageList([]), type_patches={'event': type_info('event', [], base_type='uint8')})

    def test_patched_components_and_subfields_are_resolved(self):
        types = TypeList([type_info('kind', [(0, 'a'), (1, 'b')])])
        components = [
            ComponentFieldInfo(name='low', num=None, scale=None, offset=None, units=None,
                               bits=4, bit_offset=None, accumulate=False),
            ComponentFieldInfo(name='high', num=None, scale=None, offset=None, units=None,
                               bits=4, bit_offset=None, accumulate=False),
        ]
        patch = message('packed', 400, [
            field('kind', 0, type='kind'),
            field('both', 1, components=components),
            field('low', 2),
            field('high', 3),
            field('value', 4, subfields=[subfield('value_b', 4, 'kind', 'b')]),
        ])
        message_list = MessageList([])
        self._apply(types, message_list, {400: patch})
        resolve_references(message_list, types)

        packed = message_list.messages[0]
        self.assertEqual([(c.num, c.bit_offset) for c in packed.get('both').components], [(2, 0), (3, 4)])
        ref = packed.get('value').subfields[0].ref_fields[0]
        self.assertEqual((ref.num, ref.raw_value), (0, 1))


if __name__ == '__main__':
    unittest.main()
