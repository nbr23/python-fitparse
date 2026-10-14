# patches/message_types/acclimatization.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='acclimatization',
    num=281,
    group_name='',
    fields=[
        FieldInfo(
            name='acclimatization_altitude',
            type='uint16',
            num=4,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='altitude',
            type='uint16',
            num=11,
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
