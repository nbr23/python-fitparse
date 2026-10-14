# patches/message_types/monitoring.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='monitoring',
    num=55,
    group_name='',
    fields=[
        FieldInfo(
            name='total_ascent',
            type='uint32',
            num=35,
            scale=1000.0,
            offset=None,
            units='meter',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='total_descent',
            type='uint32',
            num=36,
            scale=1000.0,
            offset=None,
            units='meter',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='moderate_activity',
            type='uint16',
            num=37,
            scale=None,
            offset=None,
            units='minutes',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='vigorous_activity',
            type='uint16',
            num=38,
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
