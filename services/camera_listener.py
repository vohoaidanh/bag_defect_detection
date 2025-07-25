import imagingcontrol4 as ic4
import queue

q = queue.Queue()

# Define a listener class to receive queue sink notifications
class Listener(ic4.QueueSinkListener):
    def __init__(self, image_queue: queue.Queue):
        self.image_queue = image_queue
        self.counter = 0

    def sink_connected(self, sink: ic4.QueueSink, image_type: ic4.ImageType, min_buffers_required: int) -> bool:
        return True

    def frames_queued(self, sink: ic4.QueueSink):
        # Lấy buffer ảnh
        buffer = sink.pop_output_buffer()

        # Lấy ảnh dưới dạng numpy array
        image = buffer.get_image()  # dạng numpy.ndarray RGB (H, W, 3)
        # print(image)
        # Đưa ảnh vào hàng đợi để xử lý YOLO
        self.image_queue.put(image)

        # Trả buffer về free queue
        buffer.release()