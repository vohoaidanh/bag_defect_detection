# actuator_interface.py
from abc import ABC, abstractmethod

class ActuatorInterface(ABC):
    @abstractmethod
    def send_trigger(self):
        pass
