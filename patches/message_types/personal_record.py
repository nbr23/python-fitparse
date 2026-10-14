# patches/message_types/personal_record.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='personal_record',
    num=114,
    group_name='',
    fields=[
        FieldInfo(
            name='metric',
            type='uint16',
            num=0,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
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
            name='record',
            type='uint32',
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
