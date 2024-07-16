import os
from ultralytics import YOLO

# Load a COCO-pretrained YOLOv8n model
model = YOLO("yolov8n.pt")

# Create the 'model' folder if it doesn't exist
if not os.path.exists("../models"):
    os.makedirs("../models")

# Save the model to the 'model' folder
model.save("../models/yolov8n.pt")

# Display model information (optional)
print(model.info())

# # Train the model on the COCO8 example dataset for 100 epochs
# results = model.train(data="coco8.yaml", epochs=100, imgsz=640)

# # Run inference with the YOLOv8n model on the 'bus.jpg' image
# results = model("path/to/bus.jpg")