# Starter Template to View YouTube Live Stream
from vidgear.gears import CamGear
import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)

stream = CamGear(
    source="https://www.youtube.com/live/2uabwdYMzVk?si=_U6BqqJuTrbrGsYf", 
    stream_mode=True,
    logging=True
).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    while True:
        frame = stream.read()
        if frame is None:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)