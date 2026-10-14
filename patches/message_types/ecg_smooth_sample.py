# patches/message_types/ecg_smooth_sample.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='ecg_smooth_sample',
    num=338,
    group_name='',
    fields=[
        FieldInfo(
            name='value',
            type='float32',
            num=0,
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
