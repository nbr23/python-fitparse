# patches/message_types/best_effort.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='best_effort',
    num=113,
    group_name='',
    fields=[
        FieldInfo(
            name='sport',
            type='enum',
            num=1,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='distance',
            type='uint32',
            num=2,
            scale=100.0,
            offset=None,
            units='meter',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='time',
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
            name='start_time',
            type='uint32',
            num=4,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='personal_record',
            type='enum',
            num=5,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
