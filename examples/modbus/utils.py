"""
modbus water supply example utils

This example models a single water tank with:
- an RTU exposing I/O via Modbus/TCP (server)
- a PLC controlling a valve via Modbus/TCP (client)
- a SCADA polling the RTU via Modbus/TCP (client)
"""

from minicps.utils import build_debug_logger


log = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir='logs/',
    suffix=''
)


# physical process parameters
GRAVITATION = 9.81          # m.s^-2 (not used directly but kept for completeness)
TANK_SECTION = 1.0          # m^2
PUMP_INFLOW = 1.0           # m^3/h when pump is ON

# Control logic thresholds (in meters)
LEVEL_THRESHOLDS_M = {
    'LL': 0.20,
    'L': 0.40,
    'H': 0.80,
    'HH': 1.00,
}

TANK_HEIGHT = 1.20          # m (saturation level)

PLC_PERIOD_SEC = 1.0        # RTU / SCADA update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0

PP_PERIOD_SEC = 1.0         # physical process update rate in seconds
PP_PERIOD_HOURS = PP_PERIOD_SEC / 3600.0

INITIAL_LEVEL = 0.50        # m


# network addresses
IP = {
    'rtu': '192.168.2.10',
    'plc': '192.168.2.15',
    'scada': '192.168.2.20',
}

MAC = {
    'rtu': '00:00:00:00:02:10',
    'plc': '00:00:00:00:02:15',
    'scada': '00:00:00:00:02:20',
}

NETMASK = '/24'


# Modbus tags
# Representation follows the WADI example: (type, offset, pid)
# - type: 'CO' (coil), 'HR' (holding register)
# - offset: integer address
# - pid: arbitrary string identifying the RTU endpoint

CO_VALVE_RTU = ('CO', 0, 'plant')   # valve command at the RTU (0=closed,1=open)
HR_LEVEL_RTU = ('HR', 0, 'plant')   # tank level at the RTU [m]


# protocol descriptions (similar to s3-2017 WADI Modbus ones)
# RTU is the Modbus server; PLC and SCADA are clients (mode 0).
PLC_PROTOCOL = {
    'name': 'modbus',
    'mode': 0,
    'server': {},
}

SCADA_PROTOCOL = {
    'name': 'modbus',
    'mode': 0,
    'server': {},
}


RTU_ADDR = IP['rtu']
RTU_TAGS = (4, 4)

RTU_SERVER = {
    'address': RTU_ADDR,
    'tags': RTU_TAGS,
}

RTU_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,
    'server': RTU_SERVER,
}


# state (SQLite) definition
NAME = 'modbus_water'
PATH = '%s.sqlite' % NAME

STATE = {
    'name': NAME,
    'path': PATH,
}

SCHEMA = """
CREATE TABLE modbus_water (
    type              TEXT NOT NULL,
    offset            INT  NOT NULL,
    pid               TEXT NOT NULL,
    value             TEXT,
    PRIMARY KEY (type, offset, pid)
);
"""

SCHEMA_INIT = """
    INSERT INTO modbus_water VALUES ('CO', 0, 'plant', '0');    -- valve CLOSED
    INSERT INTO modbus_water VALUES ('HR', 0, 'plant', '0.50'); -- initial tank level [m]
"""

