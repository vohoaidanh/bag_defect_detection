import numpy as np
import cv2
import time
from openvino.runtime import Core

# Khởi tạo OpenVINO runtime
core = Core()

# Load model
model = core.read_model("openvino_model/yolov8n.xml")
compiled_model = core.compile_model(model, "CPU")

input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)

# Danh sách ảnh đầu vào
image_paths = [
    "/home/vision/projects/bag_defect_detection/services/images/bus.jpg",
    # "/home/vision/projects/bag_defect_detection/services/images/bus.jpg"
]

# Tiền xử lý: resize + normalize
input_tensors = []
for path in image_paths:
    img = cv2.imread(path)
    img_resized = cv2.resize(img, (640, 640))
    img_tensor = np.transpose(img_resized, (2, 0, 1))  # CHW
    img_tensor = img_tensor.astype(np.float32) / 255.0
    input_tensors.append(img_tensor)

# Stack thành batch (BCHW)
input_tensor = np.stack(input_tensors, axis=0)

# Inference
start_time = time.perf_counter()
outputs = compiled_model([input_tensor])[output_layer]
end_time = time.perf_counter()

# Thời gian
elapsed_time_ms = (end_time - start_time) * 1000
print(f"Inference time for batch of {len(image_paths)} images: {elapsed_time_ms:.2f} ms")

# Output shape
print("Output shape:", outputs.shape)  # thường sẽ là (2, N, 85) với YOLOv8
