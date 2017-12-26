import numpy as np
import cv2, threading, time
import imutils
from imutils.video import WebcamVideoStream
from ANN.NeuralNetwork import *
from firebase.PyrebaseConfig import *
from objectDetection.ObjectDetection import *


'''Thread'''
def firebase_thread(flag_send, predict, firebase):
    if(flag_send % 17 == 0):
        if predict == 2:
            firebase.postData("TURN LEFT")
            print("TURN LEFT")
        elif predict == 1:
            firebase.postData("TURN RIGHT")
            print("TURN RIGHT")
        elif predict == 0:
            firebase.postData("GO FORWARD")
            print("GO FORWARD")
        elif predict == 3:
            firebase.postData("GO BACK")
            print("GO BACK")
        else:
            firebase.postData("STOP")
            print("STOP")

'''***************************  MAIN ********************************'''
'''******************************************************************'''
'''******************************************************************'''

print("[INFO] Sampling THREADED frames from camera...")
vs = WebcamVideoStream(src=1).start()

# Create neural network
model = NeuralNetwork()

# Firebase
firebase = PyrebaseConfig()

# Casscade Classifiers
# Ex: cv2.CascadeClassifier('D:/AutonomousDrivingAndy/cascade_xml/stop_sign.xml')
stop_classifier = cv2.CascadeClassifier('YOUR_PATH')

# Object Detection Instance
obj_detection = ObjectDetection()

flag_send = 1
flag_stop = True
while(True):
    try:
        # Capture frame-by-frame
        frame = vs.read()
        frame = imutils.resize(frame, width=320, height=240)
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # lower half of the image
        half_gray = gray[120:240, :]

        # Object Detection
        v_stop = obj_detection.detect(gray, stop_classifier)

        if v_stop > 100 and flag_stop is True:
            firebase.postData("STOP")
            print("STOP")
            time.sleep(5)
            flag_stop = False
        elif v_stop == 0:
            flag_stop = True

        # Display the resulting frame
        cv2.imshow('frame',half_gray)

        # reshape image
        image_array = half_gray.reshape(1, 38400).astype(np.float32)
        # neural network makes prediction
        prediction = model.predict(image_array)


        # Post Direction Command Data To Firebase
        if flag_send > 20: flag_send = 1
        flag_send += 1
        thread_FIREBASE = threading.Thread(target=firebase_thread, args=( flag_send, prediction, firebase,))
        thread_FIREBASE.start()
        thread_FIREBASE.join()


        if cv2.waitKey(1) & 0xFF == ord('q'):
            firebase.postData("STOP")
            break
    except (RuntimeError, TypeError, NameError):
        pass

# When everything done, release the capture
# do a bit of cleanup

cv2.destroyAllWindows()
vs.stop()
print("Exiting Main Thread")
