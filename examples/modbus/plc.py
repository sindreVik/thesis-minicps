"""
PLC for the Modbus water supply example.

The PLC is a Modbus client (mode 0). It:
- reads the tank level (holding register) from the RTU's Modbus server
- writes the valve command (coil) to the RTU's Modbus server
"""

import time

from minicps.devices import PLC

from utils import (
    STATE,
    PLC_PROTOCOL,
    PLC_PERIOD_SEC,
    LEVEL_THRESHOLDS_M,
    IP,
    CO_VALVE_RTU,
    HR_LEVEL_RTU,
)


RTU_ADDR = IP['rtu'] + ':502'


class WaterPLC(PLC):

    def pre_loop(self, sleep=1.0):
        time.sleep(sleep)

    def main_loop(self):
        while True:
            level = float(self.receive(HR_LEVEL_RTU, RTU_ADDR))

            # on/off (hysteresis) control:
            # - if below L: open valve
            # - if above H: close valve
            if level <= LEVEL_THRESHOLDS_M['L']:
                self.send(CO_VALVE_RTU, True, RTU_ADDR)
            elif level >= LEVEL_THRESHOLDS_M['H']:
                self.send(CO_VALVE_RTU, False, RTU_ADDR)

            time.sleep(PLC_PERIOD_SEC)


if __name__ == '__main__':

    plc = WaterPLC(
        name='plc',
        state=STATE,
        protocol=PLC_PROTOCOL,
    )

