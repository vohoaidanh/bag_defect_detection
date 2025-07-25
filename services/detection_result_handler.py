import threading
import queue
import time
from services.schemas.detection_result import DetectionResult
from services.hardware.actuator_interface import ActuatorInterface
from services.hardware.modbus_io import ModbusActuator

class DetectionResultHandler:
    def __init__(self, result_queue: queue.Queue, 
                    trigger_queue: queue.Queue, 
                    actuator: ActuatorInterface=\
                        ModbusActuator("192.168.1.100"),
                    n_delay: int = 3):

        """
        result_queue: kết quả phát hiện từ YOLO.
        trigger_queue: hàng đợi chứa trigger của sản phẩm (mỗi trigger là 1 sản phẩm đi qua).
        n_delay: số lượng trigger cần chờ trước khi kích hoạt loại bỏ.
        """
        self.result_queue = result_queue
        self.trigger_queue = trigger_queue
        self.n_delay = n_delay
        self.removal_queue = queue.Queue()  # hàng đợi lưu các sản phẩm cần loại bỏ (chờ đếm trigger)

        self.running = False
        self.start()

    def start(self):
        self.running = True
        threading.Thread(target=self._process_detection_result, daemon=True).start()
        threading.Thread(target=self._process_trigger_queue, daemon=True).start()
        

    def stop(self):
        self.running = False

    def _process_detection_result(self):
        """
        Xử lý kết quả từ YOLO, nếu sản phẩm có lỗi thì xếp vào hàng đợi loại bỏ với thông tin delay.
        """
        while self.running:
            try:
                result: DetectionResult = self.result_queue.get(timeout=0.1)
                if result.is_defect:
                    print(f"[DetectionResultHandler] Detected defect, scheduling removal after {self.n_delay} triggers.")
                    self.removal_queue.put(self.n_delay)
            except queue.Empty:
                continue

    def _process_trigger_queue(self):
        """
        Mỗi trigger tương ứng với một sản phẩm chạy qua.
        Nếu trong hàng đợi loại bỏ có phần tử, thì giảm delay đi 1.
        Khi delay == 0 thì thực hiện loại bỏ.
        """
        while self.running:
            try:
                _ = self.trigger_queue.get(timeout=0.1)

                # Cập nhật delay cho từng phần tử trong hàng đợi
                new_queue = queue.Queue()
                while not self.removal_queue.empty():
                    delay = self.removal_queue.get()
                    delay = delay - 1
                    if delay <= 0:
                        self._activate_removal()
                    else:
                        new_queue.put(delay)
                self.removal_queue = new_queue

            except queue.Empty:
                continue

    def _activate_removal(self):
        #TODO add trigger to Harware ditital output
        self.actuator.send_trigger(coil_addresses=5, pulse_time=0.3)
        print("[Handler] --> Activate reject actuator!")
