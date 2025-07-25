from ultralytics import YOLO
import cv2
import numpy as np

class YoloDetector:
    def __init__(self, model_path='yolo11n.pt'):
        self.model = YOLO(model_path)

    def predict(self, image: np.ndarray):
        # YOLO expects BGR (nếu là OpenCV) hoặc RGB (nếu dùng PIL/numpy) → phải kiểm tra
        results = self.model(image)
        return results
