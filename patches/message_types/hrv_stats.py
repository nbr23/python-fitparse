# patches/message_types/hrv_stats.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='hrv_stats',
    num=401,
    group_name='',
    fields=[
        FieldInfo(
            name='local_timestamp',
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
            name='sleep',
            type='uint16',
            num=2,
            scale=None,
            offset=None,
            units='milliseconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='target_min',
            type='uint16',
            num=3,
            scale=None,
            offset=None,
            units='milliseconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='target_max',
            type='uint16',
            num=4,
            scale=None,
            offset=None,
            units='milliseconds',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
