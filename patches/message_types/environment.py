# patches/message_types/environment.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='environment',
    num=288,
    group_name='',
    fields=[
        FieldInfo(
            name='temperature',
            type='sint8',
            num=0,
            scale=None,
            offset=None,
            units='celsius',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='humidity',
            type='sint8',
            num=1,
            scale=None,
            offset=None,
            units='percent',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment=''
)
