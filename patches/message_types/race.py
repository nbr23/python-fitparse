# patches/message_types/race.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='race',
    num=310,
    group_name='',
    fields=[
        FieldInfo(
            name='name',
            type='string',
            num=1,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='goal_time',
            type='uint32',
            num=3,
            scale=1000.0,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='goal_speed',
            type='uint16',
            num=4,
            scale=1000.0,
            offset=None,
            units='meter per second',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='distance',
            type='uint32',
            num=5,
            scale=100.0,
            offset=None,
            units='meter',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='split_count',
            type='uint16',
            num=6,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='split_distance',
            type='uint32',
            num=7,
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
