# patches/message_types/power_mode.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='power_mode',
    num=321,
    group_name='',
    fields=[
        FieldInfo(
            name='low_battery_alert',
            type='uint32',
            num=0,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='default_mode',
            type='sint32',
            num=1,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='auto_enable_time',
            type='uint32',
            num=3,
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
