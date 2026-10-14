# patches/message_types/bike_profile.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='bike_profile',
    num=6,
    group_name='',
    fields=[
        FieldInfo(
            name='color',
            type='uint8',
            num=35,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
