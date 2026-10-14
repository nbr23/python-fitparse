# patches/message_types/weather_conditions.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='weather_conditions',
    num=128,
    group_name='',
    fields=[
        FieldInfo(
            name='dew_point',
            type='sint8',
            num=15,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='uv_index',
            type='float32',
            num=16,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='air_quality',
            type='enum',
            num=17,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='atmospheric_pressure',
            type='uint32',
            num=18,
            scale=None,
            offset=None,
            units='pascal',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
