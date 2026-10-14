# patches/message_types/solar_charge.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='solar_charge',
    num=318,
    group_name='',
    fields=[
        FieldInfo(
            name='percent',
            type='uint16',
            num=0,
            scale=100.0,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='status',
            type='uint16',
            num=1,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='gain',
            type='uint32',
            num=3,
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
