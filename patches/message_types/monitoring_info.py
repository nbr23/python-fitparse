# patches/message_types/monitoring_info.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='monitoring_info',
    num=103,
    group_name='',
    fields=[
        FieldInfo(
            name='cycles_goal',
            type='uint32',
            num=7,
            scale=2.0,
            offset=None,
            units='cycles',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
