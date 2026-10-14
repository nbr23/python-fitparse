# patches/message_types/clubs.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='clubs',
    num=173,
    group_name='',
    fields=[
        FieldInfo(
            name='club_type',
            type='enum',
            num=2,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='club_nickname',
            type='string',
            num=3,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='average_distance',
            type='uint32',
            num=6,
            scale=100.0,
            offset=None,
            units='meter',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='max_distance',
            type='uint32',
            num=19,
            scale=100.0,
            offset=None,
            units='meter',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
