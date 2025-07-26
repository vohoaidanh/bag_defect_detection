from contextlib import asynccontextmanager
from fastapi import FastAPI
import queue

from services.camera_controller import CameraController
# from services.camera_simulate import CameraSimulator as CameraController
from services.yolo_processor import YoloProcessor
from services.detection_result_handler import DetectionResultHandler
from services.hardware.modbus_io import ModbusActuator
from services import detection_result_handler

@asynccontextmanager
async def lifespan(app: FastAPI):

    trigger_queue = queue.Queue(maxsize=10)
    image_queue = queue.Queue(maxsize=2)
    result_queue = queue.Queue(maxsize=2)
    last_result_queue = queue.Queue(maxsize=1)

    camera_controller = CameraController(image_queue=image_queue)
    detector = YoloProcessor(image_queue=image_queue, result_queue=result_queue)
    detection_hander = DetectionResultHandler(
        result_queue=result_queue,
        trigger_queue=trigger_queue,
        actuator=ModbusActuator("192.168.1.100"),
        n_delay=3
    )

    app.state.camera_controller = camera_controller
    app.state.detector = detector
    app.state.detection_hander = detection_hander
    app.state.image_queue = image_queue  # để endpoint upload dùng được

    yield

    print("Stopping camera thread...")
    camera_controller.stop()
    detector.stop()
    detection_hander.stop()
