# patches/message_types/true_up_body_battery.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='true_up_body_battery',
    num=464,
    group_name='',
    fields=[
        FieldInfo(
            name='snapshot_timestamp',
            type='uint32',
            num=1,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='snapshot_local_timestamp',
            type='uint32',
            num=2,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='body_battery',
            type='uint8',
            num=3,
            scale=None,
            offset=None,
            units='percent',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
