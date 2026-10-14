# patches/message_types/skin_temp_overnight.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='skin_temp_overnight',
    num=398,
    group_name='',
    fields=[
        FieldInfo(
            name='calibrated_days',
            type='uint8',
            num=3,
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
