import threading
import time
import queue
import cv2
import os
import numpy as np

class CameraSimulator:
    def __init__(self, image_queue, image_folder="services/images", interval=0.2):
        """
        image_queue: hàng đợi ảnh để gửi qua xử lý
        image_folder: nếu có thì lấy ảnh từ thư mục
        interval: thời gian giữa mỗi lần gửi ảnh
        """
        self.image_queue = image_queue
        self.image_folder = image_folder
        self.interval = interval
        self.thread = threading.Thread(target=self._simulate_stream, daemon=True)
        self.running = False

        if self.image_folder and not os.path.exists(self.image_folder):
            raise FileNotFoundError(f"Folder {self.image_folder} does not exist")
        
        # self.start()

    def start(self):
        if not self.running:
            print("camera process starting")
            self.running = True
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread.join(timeout=2)

    def _simulate_stream(self):
        image_files = []
        if self.image_folder:
            image_files = sorted([
                os.path.join(self.image_folder, f)
                for f in os.listdir(self.image_folder)
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            ])

        idx = 0
        while self.running:
            if self.image_folder and image_files:
                img = cv2.imread(image_files[idx])
                idx = (idx + 1) % len(image_files)
            else:
                # Tạo ảnh giả 640x480 ngẫu nhiên
                img = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)

            self.image_queue.put(img)
            time.sleep(self.interval)
