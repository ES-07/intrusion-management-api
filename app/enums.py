from enum import Enum, unique


@unique
class Notification_type(str, Enum):
    CALL = 'CALL'
    TXT_MSG = 'TXT_MSG'


@unique
class DeviceState(str, Enum):
    ON = 'ON'
    OFF = 'OFF'