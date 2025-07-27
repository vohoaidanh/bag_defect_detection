# queues/pipeline_queues.py

import queue
import logging

class PipelineQueues:
    def __init__(self, trigger_size=1, image_size=2, result_size=2, last_result_size=1):
        self.trigger_queue = queue.Queue(maxsize=trigger_size)
        self.image_queue = queue.Queue(maxsize=image_size)
        self.result_queue = queue.Queue(maxsize=result_size)
        self.last_result_queue = queue.Queue(maxsize=last_result_size)

        logging.info(f"Initialized queues: trigger={trigger_size}, "
                     f"image={image_size}, result={result_size}, last_result={last_result_size}")

    def put_image(self, image, timeout=1.0):
        try:
            self.image_queue.put(image, timeout=timeout)
        except queue.Full:
            logging.warning("Image queue full.")

    def get_image(self, timeout=1.0):
        try:
            return self.image_queue.get(timeout=timeout)
        except queue.Empty:
            logging.warning("Image queue empty.")
            return None

    def shutdown_all(self):
        self.image_queue.put(None)
        self.result_queue.put(None)
        self.trigger_queue.put(None)
        self.last_result_queue.put(None)
