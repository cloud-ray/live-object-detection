from vidgear.gears import CamGear
import cv2
from flask import Flask, Response, redirect, url_for
from ultralytics import YOLO
import numpy as np

app = Flask(__name__)

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")

# Initialize the video stream from YouTube
stream = CamGear(
    source="https://www.youtube.com/live/i3w7qZVSAsY?si=OFXyM14gRWZggIPP",
    stream_mode=True,
    logging=True
).start()

@app.route('/')
def index():
    return redirect(url_for('video_feed'))

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    while True:
        frame = stream.read()
        if frame is None:
            break
        
        # Perform object detection
        results = model(frame)

        # Draw bounding boxes and labels on the frame
        for result in results:  # Iterate over each result
            for box in result.boxes:  # Iterate over each box
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                conf = box.conf[0].cpu().numpy()
                cls = box.cls[0].cpu().numpy()
                label = f"{model.names[int(cls)]} {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)