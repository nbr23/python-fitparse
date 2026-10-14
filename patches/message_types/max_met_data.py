# patches/message_types/max_met_data.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='max_met_data',
    num=229,
    group_name='',
    fields=[
        FieldInfo(
            name='met_max',
            type='sint32',
            num=1,
            scale=65536.0,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='fitness_age',
            type='sint8',
            num=3,
            scale=None,
            offset=None,
            units='years',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
