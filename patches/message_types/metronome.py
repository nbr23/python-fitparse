# patches/message_types/metronome.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='metronome',
    num=152,
    group_name='',
    fields=[
        FieldInfo(
            name='enabled',
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
            name='beats_per_minute',
            type='uint8',
            num=1,
            scale=None,
            offset=None,
            units='beats per minute',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='alert_frequency',
            type='uint8',
            num=2,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='sound_and_vibe',
            type='enum',
            num=3,
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
