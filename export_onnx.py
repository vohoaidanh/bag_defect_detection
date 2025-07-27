# from ultralytics import YOLO

# model = YOLO("yolov8n.pt")

# # Perform object detection on an image
# results = model("/home/vision/projects/bag_defect_detection/services/images/bus.jpg")  # Predict on an image
# # Export the model to ONNX format for deployment
# # path = model.export(format="onnx")  # Returns the path to the exported model


# # mo --input_model yolov8n.onnx --input_shape [1,3,640,640] --output_dir openvino_model


from ultralytics import YOLO

# Load a YOLO11n PyTorch model
model = YOLO("yolov8n.pt")

results = model("/home/vision/projects/bag_defect_detection/services/images/bus.jpg")

# Export the model
# model.export(format="openvino",task="detect",imgsz=320,batch=16,int8=False,dynamic=False)  # creates 'yolo11n_openvino_model/'

# Load the exported OpenVINO model
ov_model = YOLO("/home/vision/projects/bag_defect_detection/yolov8n_openvino_model/")

# Run inference
in_put = ["/home/vision/projects/bag_defect_detection/services/images/bus.jpg",
                    "/home/vision/projects/bag_defect_detection/services/images/Explore-Vietnam-by-bike.jpg",
   
                    ]
results = ov_model(in_put +in_put+in_put+in_put+in_put +in_put+in_put+in_put)

# Run inference with specified device, available devices: ["intel:gpu", "intel:npu", "intel:cpu"]
# results = ov_model(in_put ,task="detect",device="intel:gpu")
# print(results)
