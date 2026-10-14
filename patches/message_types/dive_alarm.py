# patches/message_types/dive_alarm.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='dive_alarm',
    num=262,
    group_name='',
    fields=[
        FieldInfo(
            name='intensity',
            type='enum',
            num=13,
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
