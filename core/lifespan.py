from contextlib import asynccontextmanager
from fastapi import FastAPI
import queue


from services.camera_controller import CameraController
# from services.camera_simulate import CameraSimulator as CameraController
from services.yolo_processor import YoloProcessor
from services.detection_result_handler import DetectionResultHandler
from services.hardware.modbus_io import ModbusActuator
from services import detection_result_handler
from shared.events import SharedEvents
from shared.pipeline_queue import PipelineQueues

@asynccontextmanager
async def lifespan(app: FastAPI):

    shared_queue = PipelineQueues()
    shared_event = SharedEvents()

    camera_controller = CameraController(shared_queue=shared_queue,
                                         shared_event=shared_event)
    
    detector = YoloProcessor(shared_queue=shared_queue,
                             shared_event=shared_event)
    
    detection_hander = DetectionResultHandler(
        shared_queue=shared_queue,
        shared_event=shared_event,
        actuator=ModbusActuator("192.168.1.100"),
        n_delay=3
    )
    
    detector.start()
    detection_hander.start()

    app.state.camera_controller = camera_controller
    app.state.detector = detector
    app.state.detection_hander = detection_hander
    app.state.shared_queue = shared_queue  
    app.state.shared_event = shared_event
    yield

    print("Stopping camera thread...")
    camera_controller.stop()
    detector.stop()
    detection_hander.stop()
