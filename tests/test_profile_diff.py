#!/usr/bin/env python

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

from fitparse.records import BASE_TYPES, Field, FieldType, MessageType, ReferenceField, SubField

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from profile_diff import diff_profiles, main, render_markdown

UINT8 = BASE_TYPES[0x02]
ENUM = BASE_TYPES[0x00]


def profile(fields=None, values=None, subfields=None, mesg_name='event'):
    event_type = FieldType(name='event', base_type=ENUM, values=values or {0: 'timer'})
    data_subfields = tuple(subfields or ())
    message_fields = fields if fields is not None else {
        0: Field(name='event', type=event_type, def_num=0),
        3: Field(name='data', type=UINT8, def_num=3, subfields=data_subfields),
    }
    return (
        {'event': event_type},
        {21: MessageType(name=mesg_name, mesg_num=21, fields=message_fields)},
    )


def alert_subfield(scale=None):
    return SubField(name='alert', def_num=3, type=UINT8, scale=scale,
                    ref_fields=(ReferenceField(name='event', def_num=0, value='timer', raw_value=0),))


PROFILE_SOURCE = '''
from fitparse.records import BASE_TYPES, Field, FieldType, MessageType
FIELD_TYPES = {{'event': FieldType(name='event', base_type=BASE_TYPES[0x00], values={{0: 'timer'}})}}
MESSAGE_TYPES = {{21: MessageType(name='event', mesg_num=21, fields={{
    {fields}
}})}}
'''


class DiffProfilesTestCase(unittest.TestCase):
    def test_identical_profiles_have_no_changes(self):
        diff = diff_profiles(profile(), profile())
        self.assertFalse(diff)
        self.assertFalse(diff.breaking)
        self.assertEqual(render_markdown(diff), 'No changes to the decoded profile.\n')

    def test_added_field_and_value_are_not_breaking(self):
        old = profile()
        new = profile(values={0: 'timer', 1: 'lap'})
        new[1][21].fields[5] = Field(name='extra', type=UINT8, def_num=5)

        diff = diff_profiles(old, new)
        self.assertEqual(diff.added, ['value `event.lap` (1)', 'field `event.extra` (5)'])
        self.assertFalse(diff.breaking)

    def test_removed_field_is_breaking(self):
        old = profile()
        new = profile()
        del new[1][21].fields[3]

        diff = diff_profiles(old, new)
        self.assertEqual(diff.removed, ['field `event.data` (3)'])
        self.assertTrue(diff.breaking)

    def test_renamed_field_is_breaking(self):
        old = profile()
        new = profile()
        new[1][21].fields[3] = Field(name='payload', type=UINT8, def_num=3)

        diff = diff_profiles(old, new)
        self.assertEqual(diff.renamed, ['field `event` 3: `data` -> `payload`'])
        self.assertTrue(diff.breaking)

    def test_renamed_message_is_breaking(self):
        diff = diff_profiles(profile(), profile(mesg_name='happening'))
        self.assertEqual(diff.renamed, ['message 21: `event` -> `happening`'])

    def test_renamed_enum_value_is_breaking(self):
        diff = diff_profiles(profile(), profile(values={0: 'stopwatch'}))
        self.assertEqual(diff.renamed, ['value `event` 0: `timer` -> `stopwatch`'])
        self.assertTrue(diff.breaking)

    def test_removed_subfield_is_breaking(self):
        diff = diff_profiles(profile(subfields=[alert_subfield()]), profile())
        self.assertEqual(diff.removed, ['subfield `event.data.alert`'])

    def test_scale_change_is_reported_but_not_breaking(self):
        old = profile(subfields=[alert_subfield()])
        new = profile(subfields=[alert_subfield(scale=10)])

        diff = diff_profiles(old, new)
        self.assertEqual(diff.changed, ['subfield `event.data.alert`: scale None -> 10'])
        self.assertFalse(diff.breaking)
        self.assertIn('### Changed (1)', render_markdown(diff))


class MainTestCase(unittest.TestCase):
    def _write(self, directory, name, fields):
        path = os.path.join(directory, name)
        with open(path, 'w') as f:
            f.write(PROFILE_SOURCE.format(fields=fields))
        return path

    def _run(self, *paths):
        out = io.StringIO()
        with redirect_stdout(out):
            status = main(['profile_diff.py', *paths])
        return status, out.getvalue()

    def test_exit_status_follows_breaking_changes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = self._write(tmpdir, 'base.py', "3: Field(name='data', type=BASE_TYPES[0x02], def_num=3),")
            added = self._write(tmpdir, 'added.py', (
                "3: Field(name='data', type=BASE_TYPES[0x02], def_num=3), "
                "4: Field(name='more', type=BASE_TYPES[0x02], def_num=4),"
            ))
            renamed = self._write(tmpdir, 'renamed.py', "3: Field(name='payload', type=BASE_TYPES[0x02], def_num=3),")

            self.assertEqual(self._run(base, base)[0], 0)
            self.assertEqual(self._run(base, added)[0], 0)
            status, summary = self._run(base, renamed)
            self.assertEqual(status, 1)
            self.assertIn('`data` -> `payload`', summary)


if __name__ == '__main__':
    unittest.main()
