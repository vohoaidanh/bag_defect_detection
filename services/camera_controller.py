import imagingcontrol4 as ic4
import threading
import time
from services.camera_listener import Listener
# from yolo_processor import YoloProcessor

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
        self.stop_trigger = False
        ic4.Library.init()
        self.listener = Listener(image_queue=self.image_queue)
        self.sink = ic4.QueueSink(self.listener)
        # self.sink = ic4.SnapSink(self.listener)
  
        self.grabber = ic4.Grabber()
        self.devices = None
        self._connect_camera()

        # Start monitor thread
        self.monitor_thread = threading.Thread(target=self._monitor_camera, daemon=True)
        self.monitor_thread.start()

        # Trigger thread
        self.trigger_loop_thread = threading.Thread(target=self.trigger_loop, daemon=True)
        self.trigger_loop_thread.start()

    def _connect_camera(self):
        self.devices = ic4.DeviceEnum.devices()
        print("Devices are: ",self.devices)
        if self.devices:
            try:
                self.grabber.device_open(self.devices[0])
                print("Camera connected.")
                self.set_default_camera_settings()
                self.grabber.stream_setup(self.sink)
                print("Setup data stream from the video capture device to the sink.")
                
 
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

 
    def set_default_camera_settings(self):
        if self.grabber.is_device_open:
            self.grabber.device_property_map.set_value(ic4.PropId.WIDTH, 640)
            self.grabber.device_property_map.set_value(ic4.PropId.HEIGHT, 480)
            self.grabber.device_property_map.try_set_value(ic4.PropId.PIXEL_FORMAT, ic4.PixelFormat.BGR8)
            self.grabber.device_property_map.set_value(ic4.PropId.EXPOSURE_AUTO, "Off")
            self.grabber.device_property_map.set_value(ic4.PropId.EXPOSURE_TIME, 1000)
            # self.grabber.device_property_map.try_set_value(ic4.PropId.USER_SET_SELECTOR, "Default")
            self.grabber.device_property_map.set_value(ic4.PropId.TRIGGER_MODE, "On")
            print(self.grabber.device_property_map)



    def stop(self):
        print("Stopping camera and processing thread...")

        # 2. Dừng stream camera
        if self.grabber.is_streaming:
            self.grabber.stream_stop()

        # 3. Giải phóng thiết bị nếu cần
        if self.grabber.is_device_open:
            self.grabber.device_close()

        if not self.stop_trigger:
            self.stop_trigger =  True

        print("Camera and processing thread stopped.")

    # Hàm gửi trigger
    def trigger_loop(self):
        while not self.stop_trigger:
            try:
                if self.grabber.is_streaming:
                    self.grabber.device_property_map.execute_command(ic4.PropId.TRIGGER_SOFTWARE)
                    print("Trigger sent.")
            except Exception as e:
                print("Trigger error:", e)
            time.sleep(3)  # Đợi 3 giây



if __name__=="__main__":
    print("camera starting")
    camera_controller = CameraController()

