import imagingcontrol4 as ic4
import threading
import time
from camera_listener import Listener
# from yolo_processor import YoloProcessor
import queue

class CameraController:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(CameraController, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, image_queue):
        if self._initialized:
            return
        
        self._initialized = True
        self.image_queue = image_queue
        ic4.Library.init()
        self.listener = Listener(image_queue=self.image_queue)
        self.sink = ic4.QueueSink(self.listener)
  
        self.grabber = ic4.Grabber()
        self.devices = None
        self._connect_camera()

        # Start monitor thread
        self.monitor_thread = threading.Thread(target=self._monitor_camera, daemon=True)
        self.monitor_thread.start()

    def _connect_camera(self):
        self.devices = ic4.DeviceEnum.devices()
        if self.devices:
            try:
                self.grabber.device_open(self.devices[0])
                print("Camera connected.")
            except Exception as e:
                print("Failed to open camera:", e)
        else:
            print("No camera detected.")

    def _monitor_camera(self):
        while True:
            try:
                if not self.grabber.is_device_open:
                    print("Camera disconnected. Attempting to reconnect...")
                    self._connect_camera()
            except Exception as e:
                print("Error checking camera state:", e)
            time.sleep(5)  # check every 5 seconds

    def set_exposure(self, value: float = 5000.0):
        if self.grabber.is_device_open:
            # Configure the exposure time to 5ms (5000µs)
            self.grabber.device_property_map.set_value(ic4.PropId.EXPOSURE_AUTO, "Off")
            self.grabber.device_property_map.set_value(ic4.PropId.EXPOSURE_TIME, value)


    def get_exposure(self) -> float:
        if self.grabber.is_device_open:
            return self.grabber.get_value_float(ic4.PropId.EXPOSURE_TIME)
        return -1.0

    def set_resolution(self, width:int, height:int):
        if not self.grabber.is_device_open:
            self.grabber.device_property_map.set_value(ic4.PropId.WIDTH, width)
            self.grabber.device_property_map.set_value(ic4.PropId.HEIGHT, height)


    def stop(self):
        print("Stopping camera and processing thread...")

        # 2. Dừng stream camera
        if self.grabber.is_streaming:
            self.grabber.stream_stop()

        # 3. Giải phóng thiết bị nếu cần
        if self.grabber.is_device_open:
            self.grabber.device_close()

        print("Camera and processing thread stopped.")




if __name__=="__main__":
    print("camera starting")
    camera_controller = CameraController()
