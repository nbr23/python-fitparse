# patches/message_types/daily_altitude.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='daily_altitude',
    num=282,
    group_name='',
    fields=[
        FieldInfo(
            name='altitude',
            type='sint32',
            num=1,
            scale=65536.0,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
