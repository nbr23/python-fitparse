# patches/message_types/record_high_res.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='record_high_res',
    num=467,
    group_name='',
    fields=[
        FieldInfo(
            name='latitudes',
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
            name='longitudes',
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
            name='time_offset',
            type='uint16',
            num=4,
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
