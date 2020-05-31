from flask_mail import Mail, Message
import argparse
import threading
import time

from flask import Flask, url_for
from flask import Response
from flask import render_template
from flask import request
from imutils.video import VideoStream
from werkzeug.utils import redirect


from stream import set_flag, generate, detect_motion

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'donev.konstantin@gmail.com'
app.config['MAIL_PASSWORD'] = 'oodsgwocbkbokoif'
mail = Mail(app)

vs = VideoStream(src=0).start()
time.sleep(2.0)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        set_flag(False)
        #send_mail()
        return redirect(url_for('no_mov_exp'))
    else:
        return render_template("index.html")


@app.route("/no_mov_exp", methods=['GET', 'POST'], endpoint="no_mov_exp")
def no_mov():
    if request.method == 'POST':
        set_flag(True)
        return render_template("index.html")
    else:
        return render_template("no_mov_expected.html")


@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True)
    ap.add_argument("-o", "--port", type=int, required=True)
    ap.add_argument("-f", "--frame_count", type=int, default=32)
    args = vars(ap.parse_args())
    # args["frame_count"]

    t = threading.Thread(target=detect_motion, args=(args["frame_count"], vs, mail, app))
    t.daemon = True
    t.start()

    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)


vs.stop()
