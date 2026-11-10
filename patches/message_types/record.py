# patches/message_types/record.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='record',
    num=20,
    group_name='',
    fields=[
        FieldInfo(
            name='performance_condition',
            type='sint8',
            num=90,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment='Inferred: -7 to 9 on real runs, and never present before six minutes into the activity'
        ),
        FieldInfo(
            name='wrist_heart_rate',
            type='uint8',
            num=136,
            scale=None,
            offset=None,
            units='bpm',
            components=[],
            subfields=[],
            comment='Inferred: equals heart_rate in all but 2 of 171,509 records'
        ),
        FieldInfo(
            name='stamina_potential',
            type='uint8',
            num=137,
            scale=None,
            offset=None,
            units='percent',
            components=[],
            subfields=[],
            comment='Inferred: starts near 100 and falls over an activity, never below stamina'
        ),
        FieldInfo(
            name='stamina',
            type='uint8',
            num=138,
            scale=None,
            offset=None,
            units='percent',
            components=[],
            subfields=[],
            comment='Inferred: 1 to 100, never above stamina_potential'
        ),
        FieldInfo(
            name='body_battery',
            type='uint8',
            num=143,
            scale=None,
            offset=None,
            units='percent',
            components=[],
            subfields=[],
            comment='Inferred: within 0.3 on average of the stress_level body_battery of the same 3-minute slot'
        ),
    ],
    comment=''
)
