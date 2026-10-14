# patches/message_types/metric_summary.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='metric_summary',
    num=493,
    group_name='',
    fields=[
        FieldInfo(
            name='start',
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
            name='end',
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
            name='hr_min',
            type='uint8',
            num=8,
            scale=None,
            offset=None,
            units='beats per minute',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='daily_hr_min',
            type='uint8',
            num=10,
            scale=None,
            offset=None,
            units='beats per minute',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
