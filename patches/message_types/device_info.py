# patches/message_types/device_info.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='device_info',
    num=23,
    group_name='',
    fields=[
        FieldInfo(
            name='reception_quality',
            type='uint8',
            num=9,
            scale=None,
            offset=None,
            units='percent',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='ant_id',
            type='uint32z',
            num=24,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='ble_address',
            type='uint8',
            num=29,
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
