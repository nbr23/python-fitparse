# patches/message_types/cpe_status.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='cpe_status',
    num=394,
    group_name='',
    fields=[
        FieldInfo(
            name='status',
            type='enum',
            num=0,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='start_time',
            type='uint32',
            num=1,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='end_time',
            type='uint32',
            num=2,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
