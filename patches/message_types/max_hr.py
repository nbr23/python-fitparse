# patches/message_types/max_hr.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='max_hr',
    num=430,
    group_name='',
    fields=[
        FieldInfo(
            name='max_hr',
            type='uint8',
            num=7,
            scale=None,
            offset=None,
            units='beats per minute',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='max_hr_cycling',
            type='uint8',
            num=8,
            scale=None,
            offset=None,
            units='beats per minute',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
