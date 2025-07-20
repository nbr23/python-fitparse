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
            name='date',
            type='string',
            num=8,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment='Used to correlate UTC to system time if the timestamp of the message is in system time. This UTC time is derived from the GPS data.'
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
            name='count',
            type='uint16',
            num=3,
            scale=None,
            offset=None,
            units=None,
            components=[],
            subfields=[],
            comment=''
        ),
        FieldInfo(
            name='clock_time',
            type='uint16',
            num=4,
            scale=None,
            offset=None,
            units='min',
            components=[],
            subfields=[],
            comment='UTC timestamp used to set the devices clock and date'
        ),
    ],
    comment=''
)