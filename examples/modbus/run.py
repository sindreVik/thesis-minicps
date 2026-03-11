"""
Run script for the Modbus water supply example.

Starts a simple Mininet topology with three hosts:
- rtu: runs the RTU Modbus server
- plc: runs the PLC Modbus client (controls valve)
- scada: runs the SCADA Modbus client (polls level)

The physical process (tank) can be started separately, or on one of the hosts,
using `python physical_process.py`.
"""

import sys
from time import sleep

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info

from topo import ModbusWaterTopo


class ModbusWaterCPS(object):

    def __init__(self, name, net):

        self.name = name
        self.net = net

        self.net.start()

        # start devices
        rtu = self.net['rtu']
        plc = self.net['plc']
        scada = self.net['scada']

        SLEEP = 1.0

        # physical process (state-only)
        rtu.cmd(sys.executable + ' physical_process.py &')
        sleep(SLEEP)

        rtu.cmd(sys.executable + ' rtu.py &')
        sleep(SLEEP)

        plc.cmd(sys.executable + ' plc.py &')
        sleep(SLEEP)

        scada.cmd(sys.executable + ' scada.py &')
        sleep(SLEEP)

        info('*** Modbus water supply example running\n')
        CLI(self.net)

        self.net.stop()


if __name__ == '__main__':

    setLogLevel('info')

    topo = ModbusWaterTopo()
    net = Mininet(topo=topo)

    cps = ModbusWaterCPS(
        name='modbusWaterCPS',
        net=net,
    )

