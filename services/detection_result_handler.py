import threading
import queue
import time
from services.schemas.detection_result import DetectionResult
from services.hardware.actuator_interface import ActuatorInterface
from services.hardware.modbus_io import ModbusActuator
from shared.events import SharedEvents, EventType
from shared.pipeline_queue import PipelineQueues
from core.config import settings


class DetectionResultHandler:
    def __init__(self, shared_queue:PipelineQueues, 
                    shared_event: SharedEvents,
                    actuator: ActuatorInterface=\
                        ModbusActuator("192.168.1.100"),
                    n_delay: int = 3):

        """
        result_queue: kết quả phát hiện từ YOLO.
        n_delay: số lượng trigger cần chờ trước khi kích hoạt loại bỏ.
        """
        self._lock = threading.Lock()

        self.result_queue = shared_queue.result_queue
        self.shared_event = shared_event

        self.n_delay = n_delay
        self.removal_queue = queue.Queue()  # hàng đợi lưu các sản phẩm cần loại bỏ (chờ đếm trigger)
        self.running = False

    def start(self):

        if not self.running:
            self.running = True # Note self.runing should be set True before all thread is start
            threading.Thread(target=self._process_detection_result, daemon=True).start()
            threading.Thread(target=self._process_trigger_queue, daemon=True).start()
            

    def stop(self):
        self.running = False


    def _process_detection_result(self):
        while self.running:
            try:
                result: DetectionResult = self.result_queue.get_nowait()
                if result.is_defect(threshold=settings.CONFIDENCE_THRESHOLD):
                    print(f"[DetectionResultHandler] Detected defect, scheduling removal after {self.n_delay} triggers.")
                    self.removal_queue.put(self.n_delay)
            except queue.Empty:
                time.sleep(0.01)  # Tránh busy-wait


    def _process_trigger_queue(self):
        """
        Mỗi trigger tương ứng với một sản phẩm chạy qua.
        Nếu trong hàng đợi loại bỏ có phần tử, thì giảm delay đi 1.
        Khi delay == 0 thì thực hiện loại bỏ.
        """
        print(f"[DEBUG] Thread started: {threading.current_thread().name}, self id: {id(self)}")
        count = 0

        while self.running:
            try:
                if not self.shared_event.wait(event_type=EventType.IMAGE_RECEIVED, timeout=10.0):
                    continue

                self.shared_event.clear(event_type=EventType.IMAGE_RECEIVED)
                count += 1
                print(list(self.removal_queue.queue))
                if not self.running:
                    break

                # Cập nhật delay cho từng phần tử trong hàng đợi
                tmp_list = []

                while True:
                    try:
                        delay = self.removal_queue.get_nowait()
                        delay -= 1
                        if delay <= 0:
                            print("---------------Remove bag---------------")
                            self._activate_removal()
                        else:
                            tmp_list.append(delay)
                    except queue.Empty:
                        break

                # Đẩy lại các delay còn lại vào queue
                for delay in tmp_list:
                    try:
                        self.removal_queue.put_nowait(delay)
                    except queue.Full:
                        print("[WARNING] Removal queue is full, cannot reinsert delay item.")

            except Exception as e:
                print(f"[ERROR] Loop in image handling thread: {e}")
                time.sleep(0.01)  # Tránh busy-wait


    def _activate_removal(self):
        #TODO add trigger to Harware ditital output
        # self.actuator.send_trigger(coil_addresses=5, pulse_time=0.3)
        print("[Handler] --> Activate reject actuator!")
