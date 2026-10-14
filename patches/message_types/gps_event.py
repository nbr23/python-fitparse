# patches/message_types/gps_event.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='gps_event',
    num=326,
    group_name='',
    fields=[
        FieldInfo(
            name='event_type',
            type='uint32',
            num=0,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='data',
            type='uint32',
            num=1,
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
