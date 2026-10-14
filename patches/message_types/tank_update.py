# patches/message_types/tank_update.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='tank_update',
    num=319,
    group_name='',
    fields=[
        FieldInfo(
            name='depth',
            type='uint32',
            num=2,
            scale=None,
            offset=None,
            units='millimeter',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
