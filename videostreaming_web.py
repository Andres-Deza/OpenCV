from flask import Flask
from flask import render_template
from flask import Response
import cv2
import imutils
from imutils.video import VideoStream
import pafy
from vidgear.gears import CamGear

url="https://www.youtube.com/watch?v=Ove87nZ_1D4"
video =pafy.new(url)
best = video.getbest(preftype="webm")
stream = CamGear(source='https://www.youtube.com/watch?v=Ove87nZ_1D4', stream_mode = True, logging=False).start() # YouTube Video URL as input
# No pude encontrar rtsp en vivo asi que lo hago con este y los demas videos
# rtsp_url = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_175k.mov"
# video_stream = VideoStream(rtsp_url).start()

# while True:
#     frame = video_stream.read()
#     if frame is None:
#         continue

#     frame = imutils.resize(frame,width=1200)
#     cv2.imshow('AsimCodeCam', frame)
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break

# cv2.destroyAllWindows()
# video_stream.stop()

app = Flask(__name__)


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# capture = cv2.VideoCapture(best.url)

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades +
     "haarcascade_frontalface_default.xml")
def generate():

     while True:
          ret, frame = cap.read()
          
          if ret:
               gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
               faces = face_detector.detectMultiScale(gray, 1.3, 5)
               for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
               (flag, encodedImage) = cv2.imencode( ".jpg", frame)
               if not flag:
                    continue
               yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encodedImage) + b'\r\n')

def generate2():
     while True:
          ret2, frame2 = stream.read()
          cv2.imshow("Output Frame", frame2)
          if ret2:
                    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                    faces2 = face_detector.detectMultiScale(gray2, 1.3, 5)
                    for (x, y, w, h) in faces2:
                         cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    (flag, encodedImage) = cv2.imencode( ".jpg", frame2)
                    if not flag:
                         continue
                    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                         bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
     return render_template("index.html")
@app.route("/video_feed")
def video_feed():
     return Response(generate(),
          mimetype = "multipart/x-mixed-replace; boundary=frame")
@app.route("/video_feed2")
def video_feed2():
     return Response(generate2(),
          mimetype = "multipart/x-mixed-replace; boundary=frame")
if __name__ == "__main__":
     app.run(debug=False)
cap.release()
stream.stop()