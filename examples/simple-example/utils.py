"""
simple-example utils.py

Very small setup with two PLCs talking over Modbus.
"""

from minicps.utils import build_debug_logger


simple_logger = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir='logs/',
    suffix='',
)


# addressing
PLC1_ADDR = '10.0.0.1'
PLC2_ADDR = '10.0.0.2'

PLC1_MAC = '00:00:00:00:10:01'
PLC2_MAC = '00:00:00:00:10:02'

NETMASK = '/24'


# protocol
# tags tuple is (num_discrete_inputs, num_coils, num_input_registers, num_holding_registers)
PLC1_TAGS = (0, 0, 0, 1)  # expose a single holding register from plc1
PLC1_SERVER = {
    'address': PLC1_ADDR,
    'tags': PLC1_TAGS,
}
PLC1_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,  # tcp server + client
    'server': PLC1_SERVER,
}

# plc2 only acts as a modbus client in this example
PLC2_TAGS = (0, 0, 0, 0)
PLC2_SERVER = {
    'address': PLC2_ADDR,
    'tags': PLC2_TAGS,
}
PLC2_PROTOCOL = {
    'name': 'modbus',
    'mode': 0,  # client only
    'server': PLC2_SERVER,
}


# state (sqlite) shared by both PLCs
NAME = 'simple'
PATH = 'simple_db.sqlite'

STATE = {
    'name': NAME,
    'path': PATH,
}

SCHEMA = """
CREATE TABLE simple (
    type    TEXT    NOT NULL,
    offset  INTEGER NOT NULL,
    pid     TEXT    NOT NULL,
    value   TEXT,
    PRIMARY KEY (type, offset, pid)
);
"""

SCHEMA_INIT = """
    INSERT INTO simple VALUES ('HR', 0, 'plc1', '0');
"""

