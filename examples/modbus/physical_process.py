"""
Simple water tank physical process for the Modbus example.

The tank has a single inflow controlled by a valve. When the valve coil is ON
the tank level increases linearly based on PUMP_INFLOW. No explicit outflow
is modeled to keep the example compact.
"""

import time

from minicps.devices import Tank

from utils import (
    STATE,
    TANK_SECTION,
    INITIAL_LEVEL,
    PP_PERIOD_SEC,
    PP_PERIOD_HOURS,
    PUMP_INFLOW,
    TANK_HEIGHT,
    CO_VALVE_RTU,
    HR_LEVEL_RTU,
)


class WaterTank(Tank):

    def pre_loop(self):
        # initialize valve CLOSED and starting level
        self.set(CO_VALVE_RTU, 0)
        self.level = self.set(HR_LEVEL_RTU, INITIAL_LEVEL)

    def main_loop(self):

        while True:
            # read valve command from state (0/1)
            valve_cmd = int(self.get(CO_VALVE_RTU))

            level = float(self.get(HR_LEVEL_RTU))

            if valve_cmd == 1:
                # compute inflow volume and resulting level increase
                inflow_volume = PUMP_INFLOW * PP_PERIOD_HOURS
                level += inflow_volume / TANK_SECTION

            # saturate level between 0 and TANK_HEIGHT
            if level < 0.0:
                level = 0.0
            if level > TANK_HEIGHT:
                level = TANK_HEIGHT

            self.level = self.set(HR_LEVEL_RTU, level)

            time.sleep(PP_PERIOD_SEC)


if __name__ == '__main__':

    tank = WaterTank(
        name='water_tank',
        state=STATE,
        protocol=None,
        section=TANK_SECTION,
        level=INITIAL_LEVEL,
    )

