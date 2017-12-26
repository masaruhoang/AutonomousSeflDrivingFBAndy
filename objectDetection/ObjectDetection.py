import cv2


class ObjectDetection:
    def detect(self, resized_gray, classifier):
        # Parameter needed for Sending Data to Firebase with a delay
        v = 0

        # Detecting The Objects
        objects = classifier.detectMultiScale(resized_gray, scaleFactor=1.1,
                                              minNeighbors=5, minSize=(30, 30))

        # Draw a rectangle around the objects was found out
        for(x_axis, y_axis, width, height) in objects:
            cv2.rectangle(resized_gray, (x_axis+5, y_axis+5), (x_axis+width-5, y_axis+height-5),
                          (0, 0, 255), 2)
            #On the Camera coordinates, the y_axis pertaing to Object's point
            v = y_axis+height-5

            # Draw A Stop Text
            if width/height == 1:
                cv2.putText(resized_gray, 'STOP', (x_axis,y_axis-10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.4, (0, 0, 255), 2)
        return v
