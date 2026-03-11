"""
SCADA for the Modbus water supply example.

The SCADA periodically reads the tank level register from the RTU's Modbus
server.
"""

import time

from minicps.devices import SCADAServer

from utils import (
    STATE,
    SCADA_PROTOCOL,
    PLC_PERIOD_SEC,
    HR_LEVEL_RTU,
    IP,
)

RTU_ADDR = IP['rtu'] + ':502'

class WaterSCADA(SCADAServer):

    def pre_loop(self, sleep=1.0):
        time.sleep(sleep)

    def main_loop(self):
        while True:
            level = float(self.receive(HR_LEVEL_RTU, RTU_ADDR))
            print("SCADA: current tank level = {:.3f} m".format(level))
            time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':

    scada = WaterSCADA(
        name='scada',
        state=STATE,
        protocol=SCADA_PROTOCOL,
    )

