# patches/message_types/gnss_initialization.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='gnss_initialization',
    num=329,
    group_name='',
    fields=[
        FieldInfo(
            name='position_lat',
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
            name='position_long',
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
            name='age',
            type='uint32',
            num=2,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='altitude',
            type='float32',
            num=4,
            scale=None,
            offset=None,
            units='meter',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
