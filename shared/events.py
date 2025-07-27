from enum import Enum, auto
import threading

class EventType(Enum):
    IMAGE_RECEIVED = auto()
    DETECTION_DONE = auto()
    STOP = auto()



class SharedEvents:
    def __init__(self):
        self.events = {event: threading.Event() for event in EventType}

    def set(self, event_type: EventType):
        self.events[event_type].set()

    def clear(self, event_type: EventType):
        self.events[event_type].clear()

    def wait(self, event_type: EventType, timeout=None):
        return self.events[event_type].wait(timeout=timeout)

    def is_set(self, event_type: EventType):
        return self.events[event_type].is_set()
