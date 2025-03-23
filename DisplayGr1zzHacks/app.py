from flask import Flask, Response, render_template
import cv2
import atexit



app = Flask(__name__)

camera = cv2.VideoCapture(1)

def release_camera():
    if camera.isOpened():
        camera.release()
atexit.register(release_camera)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # MJPEG stream format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False)
