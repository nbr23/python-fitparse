#!/usr/bin/env python

import importlib.machinery
import importlib.util
import itertools
import os
import sys
from dataclasses import dataclass, field

_module_ids = itertools.count()


@dataclass
class ProfileDiff:
    added: list = field(default_factory=list)
    removed: list = field(default_factory=list)
    renamed: list = field(default_factory=list)
    changed: list = field(default_factory=list)

    @property
    def breaking(self):
        return bool(self.removed or self.renamed)

    def __bool__(self):
        return bool(self.added or self.removed or self.renamed or self.changed)


def load_profile(path):
    name = 'profile_snapshot_%d' % next(_module_ids)
    loader = importlib.machinery.SourceFileLoader(name, path)
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module.FIELD_TYPES, module.MESSAGE_TYPES


def _components(components):
    return tuple(
        (c.name, c.def_num, c.scale, c.offset, c.units, c.accumulate, c.bits, c.bit_offset)
        for c in components or ()
    )


def _field_shape(f):
    return {
        'type': f.type.name,
        'scale': f.scale,
        'offset': f.offset,
        'units': f.units,
        'components': _components(f.components),
    }


def _subfield_shape(s):
    shape = _field_shape(s)
    shape['ref_fields'] = tuple((r.def_num, r.raw_value) for r in s.ref_fields or ())
    return shape


def _describe_change(label, old_shape, new_shape):
    changes = [
        '{} {!r} -> {!r}'.format(key, old_shape[key], new_shape[key])
        for key in old_shape
        if old_shape[key] != new_shape[key]
    ]
    return '{}: {}'.format(label, ', '.join(changes)) if changes else None


def _diff_keyed(old, new, describe, diff, on_common=None):
    for key in sorted(new.keys() - old.keys()):
        diff.added.append(describe(key, new[key]))
    for key in sorted(old.keys() - new.keys()):
        diff.removed.append(describe(key, old[key]))
    for key in sorted(old.keys() & new.keys()):
        if on_common:
            on_common(key, old[key], new[key])


def _diff_types(old_types, new_types, diff):
    def common(name, old, new):
        if old.base_type.name != new.base_type.name:
            diff.changed.append('type `{}`: base_type {} -> {}'.format(name, old.base_type.name, new.base_type.name))
        old_values, new_values = old.values or {}, new.values or {}
        _diff_keyed(
            old_values, new_values,
            lambda value, label: 'value `{}.{}` ({})'.format(name, label, value),
            diff,
        )
        for value in sorted(old_values.keys() & new_values.keys()):
            if old_values[value] != new_values[value]:
                diff.renamed.append('value `{}` {}: `{}` -> `{}`'.format(
                    name, value, old_values[value], new_values[value]))

    _diff_keyed(old_types, new_types, lambda name, _: 'type `{}`'.format(name), diff, common)


def _diff_subfields(label, old_field, new_field, diff):
    old_subs = {s.name: s for s in old_field.subfields or ()}
    new_subs = {s.name: s for s in new_field.subfields or ()}

    def common(name, old, new):
        change = _describe_change('subfield `{}.{}`'.format(label, name), _subfield_shape(old), _subfield_shape(new))
        if change:
            diff.changed.append(change)

    _diff_keyed(old_subs, new_subs, lambda name, _: 'subfield `{}.{}`'.format(label, name), diff, common)


def _diff_fields(mesg_name, old_fields, new_fields, diff):
    def common(def_num, old, new):
        if old.name != new.name:
            diff.renamed.append('field `{}` {}: `{}` -> `{}`'.format(mesg_name, def_num, old.name, new.name))
        label = '{}.{}'.format(mesg_name, new.name)
        change = _describe_change('field `{}`'.format(label), _field_shape(old), _field_shape(new))
        if change:
            diff.changed.append(change)
        _diff_subfields(label, old, new, diff)

    _diff_keyed(
        old_fields, new_fields,
        lambda def_num, f: 'field `{}.{}` ({})'.format(mesg_name, f.name, def_num),
        diff, common,
    )


def _diff_messages(old_messages, new_messages, diff):
    def common(mesg_num, old, new):
        if old.name != new.name:
            diff.renamed.append('message {}: `{}` -> `{}`'.format(mesg_num, old.name, new.name))
        _diff_fields(new.name, old.fields, new.fields, diff)

    _diff_keyed(
        old_messages, new_messages,
        lambda mesg_num, m: 'message `{}` ({})'.format(m.name, mesg_num),
        diff, common,
    )


def diff_profiles(old, new):
    diff = ProfileDiff()
    _diff_types(old[0], new[0], diff)
    _diff_messages(old[1], new[1], diff)
    return diff


def render_markdown(diff):
    if not diff:
        return 'No changes to the decoded profile.\n'
    sections = [
        ('Removed', diff.removed),
        ('Renamed', diff.renamed),
        ('Added', diff.added),
        ('Changed', diff.changed),
    ]
    out = ['## Profile changes', '']
    if diff.breaking:
        out += ['**Removals or renames: this update breaks existing consumers and needs a patch or a manual decision.**', '']
    for title, entries in sections:
        if entries:
            out += ['### {} ({})'.format(title, len(entries)), '']
            out += ['- {}'.format(entry) for entry in entries]
            out.append('')
    return '\n'.join(out)


def main(argv):
    if len(argv) != 3:
        print('Usage: %s <old profile.py> <new profile.py>' % os.path.basename(argv[0]), file=sys.stderr)
        return 2
    diff = diff_profiles(load_profile(argv[1]), load_profile(argv[2]))
    sys.stdout.write(render_markdown(diff))
    return 1 if diff.breaking else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
