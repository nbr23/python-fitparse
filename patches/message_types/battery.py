# patches/message_types/battery.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='battery',
    num=104,
    group_name='',
    fields=[
        FieldInfo(
            name='battery_voltage',
            type='uint16',
            num=0,
            scale=1000.0,
            offset=None,
            units='volt',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='current',
            type='sint16',
            num=1,
            scale=1000.0,
            offset=None,
            units='ampere',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='temperature',
            type='sint8',
            num=3,
            scale=None,
            offset=None,
            units='celsius',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
