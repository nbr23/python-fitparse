# patches/message_types/functional_metrics.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='functional_metrics',
    num=356,
    group_name='',
    fields=[
        FieldInfo(
            name='functional_threshold_power',
            type='uint16',
            num=4,
            scale=None,
            offset=None,
            units='watt',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='running_lactate_threshold_power',
            type='uint16',
            num=7,
            scale=None,
            offset=None,
            units='watt',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='running_lactate_threshold_hr',
            type='uint8',
            num=8,
            scale=None,
            offset=None,
            units='beats per minute',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='cycling_lactate_threshold_hr',
            type='uint8',
            num=9,
            scale=None,
            offset=None,
            units='beats per minute',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
