# patches/message_types/true_up_recovery.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='true_up_recovery',
    num=357,
    group_name='',
    fields=[
        FieldInfo(
            name='stamina_potential_load',
            type='uint8',
            num=0,
            scale=None,
            offset=None,
            units='percent',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='stamina_potential_distance',
            type='uint8',
            num=1,
            scale=None,
            offset=None,
            units='percent',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='recovery_time',
            type='uint16',
            num=2,
            scale=None,
            offset=None,
            units='minutes',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
