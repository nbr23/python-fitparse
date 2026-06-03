# patches/message_types/stress_level.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='stress_level',
    num=227,
    group_name='',
    fields=[
        FieldInfo(
            name='body_battery',
            type='sint8',
            num=3,
            scale=None,
            offset=None,
            units='percent',
            components=[],
            subfields=[],
            comment='Undocumented Garmin Body Battery level (0-100)'
        ),
    ],
    comment=''
)
