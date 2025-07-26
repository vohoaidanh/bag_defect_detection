import imagingcontrol4 as ic4
import queue
import os
from shared.image_data import ImageWithMeta
import cv2

q = queue.Queue()

# Define a listener class to receive queue sink notifications
class Listener(ic4.QueueSinkListener):
    def __init__(self, image_queue: queue.Queue):
        self.image_queue = image_queue
        self.counter = 0
        # self.image_type = ic4.ImageType(ic4.imagetype.PixelFormat.BGR8)

    def sink_connected(self, sink: ic4.QueueSink, image_type: ic4.ImageType, min_buffers_required: int) -> bool:
        return True

    def frames_queued(self, sink: ic4.QueueSink):
        # Lấy buffer ảnh
        buffer = sink.pop_output_buffer()
        
        self.counter+=1

	    # Save the image buffer's contents in a BMP file
        home_dir = "/home/vision/projects"
        file_name = os.path.join(home_dir, f"{self.counter}.bmp")
        buffer.save_as_png(file_name)
           
        
        # Lấy ảnh dưới dạng numpy array
        image = buffer.numpy_wrap()  # dạng numpy.ndarray RGB (H, W, 3)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        image = ImageWithMeta(image)

        # Đưa ảnh vào hàng đợi để xử lý YOLO
        self.image_queue.put(image)

        # Trả buffer về free queue
        buffer.release()