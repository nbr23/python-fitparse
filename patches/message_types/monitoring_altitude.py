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
            scale=5.0,
            offset=500.0,
            units='meter',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
