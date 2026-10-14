# patches/message_types/music_info.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='music_info',
    num=243,
    group_name='',
    fields=[
        FieldInfo(
            name='start_time',
            type='uint32',
            num=0,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='title',
            type='string',
            num=2,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='artist',
            type='string',
            num=3,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='genre',
            type='string',
            num=4,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='duration',
            type='uint16',
            num=5,
            scale=None,
            offset=None,
            units='seconds',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
