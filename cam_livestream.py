from flask import Flask, render_template, Response 
from picamera2 import Picamera2
import cv2

# ───── Setup Camera ─────
app = Flask(__name__)
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (1280, 720), "format": "XRGB8888"}))
camera.set_controls({"FrameDurationLimits": (16666, 16666), "AeEnable": False, "ExposureTime": 10000})
camera.start()

# ───── Frame generator ─────
def gen_frames():
    while True:
        frame = camera.capture_array()

        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Cache-Control: no-cache\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# ───── Flask Routes ─────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='10.42.0.1', port=5000)
