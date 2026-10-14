# patches/message_types/audio_prompts.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='audio_prompts',
    num=266,
    group_name='',
    fields=[
        FieldInfo(
            name='lap_alerts',
            type='enum',
            num=1,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='dialect',
            type='enum',
            num=10,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='activity_alerts',
            type='enum',
            num=12,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='workout_alerts',
            type='enum',
            num=18,
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
