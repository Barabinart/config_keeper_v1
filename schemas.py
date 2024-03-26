from enum import Enum
from pydantic import BaseModel


class TypesOfDevices(Enum):
    cisco_ios = "cisco_ios"
    eltex = "eltex"
    mikrotik_routeros = 'mikrotik_routeros'


class Authdata(BaseModel):
    device_type: TypesOfDevices = "cisco_ios"
    device_ip: str
    username: str
    password: str
