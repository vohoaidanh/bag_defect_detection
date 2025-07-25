import threading
import queue

from torch import igamma
from services.yolo_detector import YoloDetector
from shared.utils import parse_yolo_result
from services.schemas.detection_result import DetectionResult
from shared.image_data import ImageWithMeta
from shared.utils import safe_queue_put

from core.config import settings


class YoloProcessor:
    _instance = None
    _lock = threading.Lock()  # Đảm bảo thread-safe

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(YoloProcessor, cls).__new__(cls)
        return cls._instance

    def __init__(self, image_queue: queue.Queue, result_queue: queue.Queue):
        if hasattr(self, "_initialized") and self._initialized:
            return  # Không khởi tạo lại nếu đã init rồi

        self.image_queue = image_queue
        self.result_queue = result_queue

        self.model = YoloDetector(model_path=settings.MODEL_PATH)
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        self._initialized = True

    def _run(self):
        print("YoloProcessor started.")
        while self.running:
            try:
                data_input = self.image_queue.get(timeout=2)
                if isinstance(data_input,ImageWithMeta):
                    image = data_input.image
                else:
                    print(f"Warning: Expected type ImageWithMeta but got {type(data_input)}")
                    continue

                result = self.model.predict(image)
                detection_result: DetectionResult = parse_yolo_result(result)
                detection_result.id = data_input.id
                safe_queue_put(self.result_queue, detection_result, DetectionResult)
                # for r in results:
                #     print("Detected boxes:", r.boxes.xyxy)

            except queue.Empty:
                continue
            except Exception as e:
                print("Error in YOLO processing:", e)

    def stop(self):
        self.running = False
        self.thread.join(timeout=2)
