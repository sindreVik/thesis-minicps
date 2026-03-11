"""
RTU for the Modbus water supply example.

The RTU:
- exposes its tags through a Modbus server
- does not implement control logic (the PLC does that)
"""

import time

from minicps.devices import RTU

from utils import (
    STATE,
    RTU_PROTOCOL,
    PLC_PERIOD_SEC,
)


class WaterRTU(RTU):

    def pre_loop(self, sleep=1.0):
        time.sleep(sleep)

    def main_loop(self):
        while True:
            time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':

    rtu = WaterRTU(
        name='rtu',
        state=STATE,
        protocol=RTU_PROTOCOL,
    )

