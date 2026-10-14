# patches/message_types/capabilities.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='capabilities',
    num=1,
    group_name='',
    fields=[
        FieldInfo(
            name='wifi',
            type='enum',
            num=24,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='audio_prompts',
            type='uint32z',
            num=26,
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
