from services.schemas.detection_result import DetectionResult, Detection
from queue import Queue
from typing import TypeVar, Type, Generic

def parse_yolo_result(results) -> DetectionResult:
    """
    Chuyển kết quả YOLOv8 sang DetectionResult dạng đơn giản.
    """
    image_with_boxes = results[0].plot()

    detections = []
    names = results[0].names
    boxes = results[0].boxes

    for i in range(len(boxes)):
        cls_id = int(boxes.cls[i].item())
        conf = float(boxes.conf[i].item())
        bbox = tuple(map(int, boxes.xyxy[i].tolist()))  # (x1, y1, x2, y2)

        detection = Detection(
            label=names[cls_id],
            confidence=conf,
            bbox=bbox
        )
        detections.append(detection)

    return DetectionResult(
        detections=detections,
        image_with_boxes=image_with_boxes
    )



import yaml
import os

def load_config(path="config.yaml"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file '{path}' not found.")
    
    with open(path, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error YAML file: {e}")

    return config

T = TypeVar('T')
def safe_queue_put(queue: Queue, data: T, expected_type: Type[T]):
    if not isinstance(data, expected_type):
        raise TypeError(f"Invalid type: expected {expected_type.__name__}, got {type(data).__name__}")
    queue.put(data)