# patches/message_types/training_balance_results.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='training_balance_results',
    num=294,
    group_name='',
    fields=[
        FieldInfo(
            name='monthly_load_aerobic_low',
            type='sint32',
            num=0,
            scale=65536.0,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='monthly_load_aerobic_high',
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
            name='monthly_load_anaerobic',
            type='sint32',
            num=2,
            scale=65536.0,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='monthly_load_anaerobic_target_min',
            type='uint16',
            num=7,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='monthly_load_anaerobic_target_max',
            type='uint16',
            num=8,
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
