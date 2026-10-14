# patches/message_types/hr_minimum.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='hr_minimum',
    num=431,
    group_name='',
    fields=[
        FieldInfo(
            name='day',
            type='uint16',
            num=1,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='local_timestamp',
            type='uint32',
            num=2,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='hr_min',
            type='uint8',
            num=3,
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
