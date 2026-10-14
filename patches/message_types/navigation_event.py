# patches/message_types/navigation_event.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='navigation_event',
    num=261,
    group_name='',
    fields=[
        FieldInfo(
            name='type',
            type='enum',
            num=0,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='latitude',
            type='sint32',
            num=1,
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
            num=2,
            scale=None,
            offset=None,
            units='semicircles',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='data',
            type='uint32',
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
