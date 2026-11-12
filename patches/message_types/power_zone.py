# patches/message_types/power_zone.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='power_zone',
    num=9,
    group_name='',
    fields=[
        FieldInfo(
            name='timestamp',
            type='date_time',
            num=253,
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