# patches/message_types/open_water_event.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='open_water_event',
    num=89,
    group_name='',
    fields=[
        FieldInfo(
            name='event_type',
            type='enum',
            num=0,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='fractional_timestamp',
            type='uint16',
            num=1,
            scale=32768.0,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='swim_stroke',
            type='uint32',
            num=5,
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
