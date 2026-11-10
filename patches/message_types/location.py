# patches/message_types/location.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='location',
    num=29,
    group_name='',
    fields=[
        FieldInfo(
            name='name',
            type='string',
            num=0,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment='Label shown on the device, defaults to the save date and time (e.g. 22 Feb 15:12)'
        ),
        FieldInfo(
            name='position_lat',
            type='sint32',
            num=1,
            scale=None,
            offset=None,
            units='semicircles',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='position_long',
            type='sint32',
            num=2,
            scale=None,
            offset=None,
            units='semicircles',
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='altitude',
            type='uint16',
            num=4,
            scale=5,
            offset=500,
            units='m',
            components=[],
            subfields=[],
            comment='Inferred from saved locations: values follow the standard FIT altitude encoding'
        ),
        FieldInfo(
            name='message_index',
            type='message_index',
            num=254,
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
