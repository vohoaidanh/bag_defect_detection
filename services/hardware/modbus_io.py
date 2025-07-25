from services.hardware.actuator_interface import ActuatorInterface
from pymodbus.client import ModbusTcpClient
from typing import List, Union
import time

class ModbusActuator(ActuatorInterface):
    def __init__(self, ip: str, port: int = 502):
        self.client = ModbusTcpClient(ip, port=port)
        

    def send_trigger(self, coil_addresses: Union[int, List[int]], pulse_time: float = 0.3):
        if isinstance(coil_addresses, int):
            coil_addresses = [coil_addresses]

        for addr in coil_addresses:
            self.client.write_coil(addr, True)
        time.sleep(pulse_time)
        for addr in coil_addresses:
            self.client.write_coil(addr, False)
