# run_camera_yolo.py
# from camera_controller import CameraController
from camera_simulate import CameraSimulator
from yolo_processor import YoloProcessor
import queue
import time

if __name__ == "__main__":

    image_queue = queue.Queue(maxsize=2)
    # camera = CameraController(image_queue=image_queue)
    camera = CameraSimulator(image_queue=image_queue, image_folder="app/images", interval=2)
    camera.start()
    detector = YoloProcessor(image_queue=image_queue)


    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")
        camera.stop()
        detector.stop()
