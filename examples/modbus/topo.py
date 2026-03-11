"""
Modbus water supply topology.

Three hosts connected to a single switch:
- rtu: field device exposing I/O via Modbus (server)
- plc: PLC controlling the valve via Modbus (client)
- scada: SCADA polling level via Modbus (client)
"""

from mininet.topo import Topo

from utils import IP, MAC, NETMASK


class ModbusWaterTopo(Topo):

    def build(self):

        switch = self.addSwitch('s1')

        rtu = self.addHost(
            'rtu',
            ip=IP['rtu'] + NETMASK,
            mac=MAC['rtu'])
        self.addLink(rtu, switch)

        plc = self.addHost(
            'plc',
            ip=IP['plc'] + NETMASK,
            mac=MAC['plc'])
        self.addLink(plc, switch)

        scada = self.addHost(
            'scada',
            ip=IP['scada'] + NETMASK,
            mac=MAC['scada'])
        self.addLink(scada, switch)


