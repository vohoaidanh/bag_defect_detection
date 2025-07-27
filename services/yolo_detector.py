from ultralytics import YOLO
import numpy as np

class YoloDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, image: np.ndarray):
        # YOLO expects BGR (penCV) hoặc RGB (PIL/numpy)
        results = self.model(image)
        return results
