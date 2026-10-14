# patches/message_types/metric_recovery.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='metric_recovery',
    num=284,
    group_name='',
    fields=[
        FieldInfo(
            name='recovery_minutes',
            type='uint16',
            num=0,
            scale=None,
            offset=None,
            units='minutes',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='recovery_start',
            type='uint32',
            num=1,
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
