import imagingcontrol4 as ic4
import queue
import os
from shared.image_data import ImageWithMeta
import cv2
import time
from shared.events import SharedEvents, EventType
from shared.pipeline_queue import PipelineQueues

q = queue.Queue()

# Define a listener class to receive queue sink notifications
class Listener(ic4.QueueSinkListener):
    def __init__(self, shared_queue: PipelineQueues, shared_event:SharedEvents):
        self.image_queue = shared_queue.image_queue
        self.counter = 0
        self.shared_event = shared_event

    def sink_connected(self, sink: ic4.QueueSink, image_type: ic4.ImageType, min_buffers_required: int) -> bool:
        return True

    def frames_queued(self, sink: ic4.QueueSink):
        # Lấy buffer ảnh
        buffer = sink.pop_output_buffer()
        self.counter+=1

        # Lấy ảnh dưới dạng numpy array
        image = buffer.numpy_wrap()  # dạng numpy.ndarray RGB (H, W, 3)
        image = cv2.cvtColor(image, cv2.COLOR_BayerGR2RGB)
        # print(image.shape)

        home_dir = "/home/vision/projects/images"
        file_name = os.path.join(home_dir, f"{self.counter}.png")
        cv2.imwrite(file_name, image)

        image = ImageWithMeta(image)

        # # Đưa ảnh vào hàng đợi để xử lý YOLO
        # self.shared_event.set(event_type=EventType.IMAGE_RECEIVED)
        try:
            self.image_queue.put(image)
            self.shared_event.set(event_type=EventType.IMAGE_RECEIVED)
        except queue.Full:
            print("Warning: image_queue is full. Dropping frame.")

        #         # Trả buffer về free queue
        buffer.release()
