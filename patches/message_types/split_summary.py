# patches/message_types/split_summary.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='split_summary',
    num=313,
    group_name='',
    fields=[
        FieldInfo(
            name='paceband_target_time',
            type='uint32',
            num=61,
            scale=1000.0,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='paceband_target_distance',
            type='uint32',
            num=62,
            scale=100.0,
            offset=None,
            units='meter',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='paceband_target_speed',
            type='uint16',
            num=63,
            scale=1000.0,
            offset=None,
            units='meter per second',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='max_stress',
            type='uint16',
            num=73,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='split_score_card_index',
            type='uint16',
            num=76,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='step_speed_loss',
            type='uint16',
            num=83,
            scale=100.0,
            offset=None,
            units='centimeter per second',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='step_speed_loss_percentage',
            type='uint16',
            num=84,
            scale=100.0,
            offset=None,
            units='percent',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
