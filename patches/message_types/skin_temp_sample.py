# patches/message_types/skin_temp_sample.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from generate_profile import MessageInfo, FieldInfo

MESSAGE_INFO = MessageInfo(
    name='skin_temp_sample',
    num=397,
    group_name='',
    fields=[
        FieldInfo(
            name='deviation',
            type='float32',
            num=1,
            scale=None,
            offset=None,
            units='C',
            components=[],
            subfields=[],
            comment='Inferred: one per minute over the day before skin_temp_overnight, -11 to +5; '
                    'the baseline is unconfirmed, the sleep-window mean sits about 1 C below average_deviation'
        ),
        FieldInfo(
            name='timestamp',
            type='date_time',
            num=253,
            scale=None,
            offset=None,
            units='s',
            components=[],
            subfields=[],
            comment=''
        ),
    ],
    comment='Undocumented per-minute skin temperature, found only in SkinTemp files'
)
