# patches/message_types/metrics_time.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='metrics_time',
    num=241,
    group_name='',
    fields=[
        FieldInfo(
            name='local_timestamp',
            type='uint32',
            num=0,
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
