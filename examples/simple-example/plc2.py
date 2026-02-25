"""
simple-example plc2.py

PLC2 acts as a Modbus client and periodically reads the holding
register exposed by PLC1.
"""

import time

from minicps.devices import PLC
from utils import STATE, PLC2_PROTOCOL, PLC1_ADDR


# holding register 0 on plc1
HR_0_PLC1 = ('HR', 0, 'plc1')

# full Modbus TCP address (ip:port) of plc1 server
PLC1_SERVER_ADDR = PLC1_ADDR + ':502'


class SimplePLC2(PLC):

    def pre_loop(self, sleep=0.5):
        print('simple-example: plc2 pre_loop')
        time.sleep(sleep)

    def main_loop(self, sleep=1.0):
        print('simple-example: plc2 main_loop')

        while True:
            value = self.receive(HR_0_PLC1, PLC1_SERVER_ADDR)
            print('plc2 read HR[0] from plc1 = {}'.format(value))
            time.sleep(sleep)


if __name__ == "__main__":

    plc2 = SimplePLC2(
        name='plc2',
        state=STATE,
        protocol=PLC2_PROTOCOL,
    )

