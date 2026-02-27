"""
simple-example run.py

Starts a tiny Mininet topology with two PLCs and runs the Modbus
example on them.
"""

import sys

from mininet.net import Mininet
from mininet.cli import CLI

from minicps.mcps import MiniCPS
from topo import SimpleTopo


class SimpleCPS(MiniCPS):
    """Main container used to run the simple Modbus simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        self.net.start()

        # start PLC processes
        plc1, plc2 = self.net.get('plc1', 'plc2')
        plc1.cmd(sys.executable + ' plc1.py &> logs/plc1.log &')
        plc2.cmd(sys.executable + ' plc2.py &> logs/plc2.log &')

        CLI(self.net)

        self.net.stop()


if __name__ == "__main__":

    topo = SimpleTopo()
    net = Mininet(topo=topo)

    simple_cps = SimpleCPS(
        name='simpleCPS',
        net=net,
    )

