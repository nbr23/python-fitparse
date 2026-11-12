# patches/message_types/monitoring_altitude.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='monitoring_altitude',
    num=279,
    group_name='',
    fields=[
        FieldInfo(
            name='altitude',
            type='uint32',
            num=0,
            scale=5,
            offset=500,
            units='meter',
            components=[],
            subfields=[],
            comment=''
        ),
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