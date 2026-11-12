# patches/message_types/end_of_file.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='end_of_file',
    num=276,
    group_name='',
    fields=[
        FieldInfo(
            name='timestamp',
            type='date_time',
            num=253,
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