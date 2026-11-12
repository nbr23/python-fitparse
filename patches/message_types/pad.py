# patches/message_types/pad.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='pad',
    num=105,
    group_name='',
    fields=[
    ],
    comment=''
)