# patches/message_types/incident_detection.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='incident_detection',
    num=195,
    group_name='',
    fields=[
        FieldInfo(
            name='latitude',
            type='sint32',
            num=0,
            scale=None,
            offset=None,
            units='semicircles',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='longitude',
            type='sint32',
            num=1,
            scale=None,
            offset=None,
            units='semicircles',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
