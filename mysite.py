from flask import Flask, render_template, Response, request, redirect, url_for, session
import numpy as np
import mysql.connector
import cv2

'''CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                       "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                       "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                       "sofa", "train", "tvmonitor"]'''

CLASSES = ["", "", "", "", "",
            "", "", "car", "", "", "", "",
            "", "", "", "", "", "",
            "", "", ""]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES)))

# load our serialized model from disk
# print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
img = ''

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

# Set the secret key for sessions
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Define a function to check if a user is logged in
def is_logged_in():
    return 'username' in session

# Connect to the MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Ashpak@2002",
  database="parkingdetails"
)

# Define a function to check if a user's credentials are valid
def is_valid_login(username, password):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    val = (username, password)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return True
    else:
        return False


# Define the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect them to the camera page
    if is_logged_in():
        return redirect(url_for('camera'))

    # If the user submitted the login form, check their credentials and log them in if they're valid
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_valid_login(username, password):
            session['username'] = username
            return redirect(url_for('camera'))
        else:
            return render_template('login.html', error='Invalid username or password')

    # If the user didn't submit the login form yet, display the login form
    return render_template('login.html')

# Define the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if is_logged_in():
        return redirect(url_for('camera'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')

        mycursor = mydb.cursor()
        sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        val = (username, password, email)
        mycursor.execute(sql, val)
        mydb.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def camera():
    if not is_logged_in():
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['submit_button'] == 'Slot Details':
            return redirect(url_for('slots'))
    return render_template('camera.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

def get_frame():
    global img
    a1, b1, c1, d1, e1, f1 = 1, 1, 1, 1, 1, 1
    get_frame.a, get_frame.b, get_frame. c, get_frame.d, get_frame.e, get_frame.f = 1, 1, 1, 1, 1, 1
    camera = cv2.VideoCapture(0)                                        # this makes a web cam object

    while True:
        ret, img = camera.read()
        cv2.line(img, (0, 200), (640, 200), (0, 0, 255))
        cv2.line(img, (213, 0), (213, 480), (0, 0, 255))
        cv2.line(img, (426, 0), (426, 480), (0, 0, 255))


        (h, w) = img.shape[:2]
        # cv2.dnn.blobFromImage() function is used to preprocess the input image for the object detection model
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if (confidence > 0.2):
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                label = CLASSES[idx]
                cv2.rectangle(img, (startX, startY), (endX, endY), COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(img, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                if label == 'car':
                    if (endY < 240):
                        if (endX < 213):
                            a1 = 0
                        elif (endX < 426):
                            b1 = 0
                        elif (endX < 640):
                            c1 = 0
                    else:
                        if (endX < 213):
                            d1 = 0
                        elif (endX < 426):
                            e1 = 0
                        else:
                            f1 = 0

        if(a1==0):
            get_frame.a = 0
            status1 = 'Not Available'
            colour1 = (0, 0, 255)
        else:
            get_frame.a = 1
            status1 = 'Available'
            colour1 = (0, 255, 0)

        if (b1 == 0):
            get_frame.b = 0
            status2 = 'Not Available'
            colour2 = (0, 0, 255)
        else:
            get_frame.b = 1
            status2 = 'Available'
            colour2 = (0, 255, 0)

        if (c1 == 0):
            get_frame.c = 0
            status3 = 'Not Available'
            colour3 = (0, 0, 255)
        else:
            get_frame.c = 1
            status3 = 'Available'
            colour3 = (0, 255, 0)

        if (d1 == 0):
            get_frame.d = 0
            status4 = 'Not Available'
            colour4 = (0, 0, 255)
        else:
            get_frame.d = 1
            status4 = 'Available'
            colour4 = (0, 255, 0)

        if (e1 == 0):
            get_frame.e = 0
            status5 = 'Not Available'
            colour5 = (0, 0, 255)
        else:
            get_frame.e = 1
            status5 = 'Available'
            colour5 = (0, 255, 0)

        if (f1 == 0):
            get_frame.f = 0
            status6 = 'Not Available'
            colour6 = (0, 0, 255)
        else:
            get_frame.f = 1
            status6 = 'Available'
            colour6 = (0, 255, 0)

        cv2.putText(img, status1, (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour1, 2)
        cv2.putText(img, status2, (223, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour2, 2)
        cv2.putText(img, status3, (436, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour3, 2)
        cv2.putText(img, status4, (10, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour4, 2)
        cv2.putText(img, status5, (223, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour5, 2)
        cv2.putText(img, status6, (436, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour6, 2)

        imgencode = cv2.imencode('.jpg', img)[1]
        stringData = imgencode.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')
        a1,b1,c1,d1,e1,f1 = 1,1,1,1,1,1


@app.route('/video_stream')
def video_stream():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/slots')
def slots():
    return render_template('slot.html', data = [[get_frame.a, get_frame.b, get_frame.c], [get_frame.d, get_frame.e, get_frame.f]])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
