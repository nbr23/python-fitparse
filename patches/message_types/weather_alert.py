# patches/message_types/weather_alert.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='weather_alert',
    num=129,
    group_name='',
    fields=[
        FieldInfo(
            name='position_lat',
            type='sint32',
            num=5,
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
            num=6,
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
