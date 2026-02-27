"""
simple-example plc1.py

PLC1 exposes a single Modbus holding register and periodically
writes an increasing counter to it.
"""

import time

from minicps.devices import PLC
from utils import STATE, PLC1_PROTOCOL, PLC1_ADDR


# holding register 0 on plc1
HR_0_PLC1 = ('HR', 0, 'plc1')

# full Modbus TCP address (ip:port) of plc1 server
PLC1_SERVER_ADDR = PLC1_ADDR + ':502'


class SimplePLC1(PLC):

    def pre_loop(self, sleep=0.5):
        print('simple-example: plc1 pre_loop')
        time.sleep(sleep)

    def main_loop(self, sleep=3.0):
        print('simple-example: plc1 main_loop')
        value = 0

        while True:
            # write the current value to the local Modbus server
            self.send(HR_0_PLC1, value, PLC1_SERVER_ADDR)
            print('plc1 wrote HR[0] = {}'.format(value))

            value += 1
            time.sleep(sleep)


if __name__ == "__main__":

    plc1 = SimplePLC1(
        name='plc1',
        state=STATE,
        protocol=PLC1_PROTOCOL,
    )

