# patches/message_types/race_prediction.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='race_prediction',
    num=339,
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
            name='time_5k',
            type='uint16',
            num=1,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='time_10k',
            type='uint16',
            num=2,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='time_half_marathon',
            type='uint16',
            num=3,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='time_full_marathon',
            type='uint16',
            num=4,
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
