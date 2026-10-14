# patches/message_types/sleep_demand.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='sleep_demand',
    num=410,
    group_name='',
    fields=[
        FieldInfo(
            name='normal',
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
            name='demand',
            type='uint16',
            num=1,
            scale=None,
            offset=None,
            units='minutes',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='start',
            type='uint16',
            num=7,
            scale=None,
            offset=None,
            units='minutes',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='end',
            type='uint16',
            num=8,
            scale=None,
            offset=None,
            units='minutes',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
