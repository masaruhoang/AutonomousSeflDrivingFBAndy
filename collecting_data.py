from firebase.PyrebaseConfig import *
import numpy as np
import pygame,cv2,os
from imutils.video import WebcamVideoStream
import imutils

'''*******************INIT***********************'''
temp_label = np.zeros((1, 3), 'float')
saved_frame = 0
total_frame = 0

#Init Pygame for steering input
pygame.init()
pygame.display.set_mode((100,100))

# Create class labels (Left, Right, Forward, Back)
direction = np.zeros((3,3), 'float')
for i in range(3):
    direction[i, i] = 1

# Collect images for training
print('Start Collecting data..........')
time0 = cv2.getTickCount()
image_array = np.zeros((1, 38400))
label_array = np.zeros((1, 3), 'float')

complex_cmd = False


'''*******************MAIN***********************'''
'''**********************************************'''
#Camera will warm up in background thread
vs = WebcamVideoStream(src=0).start()

# Firebase
firebase = PyrebaseConfig()

#Stream Video frames

try:
    #The number of the frame will be counted
    frameInd = 1
    while(True):
        # Capture frame-by-frame
        frame = vs.read()
        frame = imutils.resize(frame, width=320, height=240)

        #Convert frame -> GrayScacle
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Select the lower half of the images
        half_gray = gray[120:240, :]

        # Display the resulting frame
        cv2.imshow('Resized Image',half_gray)

        # reshape the roi image into one row array
        temp_array = half_gray.reshape(1, 38400).astype(np.float32)


        # Get Driver Input Annually
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or complex_cmd:
                key = pygame.key.get_pressed()
                complex_cmd = False
                print("Collecting...")

                # only save the images where there is user action
                cv2.imwrite('dataset_images/frame{:>05}.jpg'.format(frameInd), half_gray)

                # simple orders
                if key[pygame.K_UP]:
                    print("Forward - " + str(frameInd))
                    firebase.postData("GO FORWARD")

                elif key[pygame.K_DOWN]:
                    print("Back - " + str(frameInd))
                    firebase.postData("GO BACK")

                elif key[pygame.K_RIGHT]:
                    print("Right - " +str(frameInd))
                    firebase.postData("TURN RIGHT")


                elif key[pygame.K_LEFT]:
                    print("Left - " +str(frameInd))
                    firebase.postData("TURN LEFT")

                elif key[pygame.K_BACKSPACE]:
                    image_array = np.vstack((image_array, temp_array))
                    label_array = np.vstack((label_array, direction[2]))
                    saved_frame += 1
                    frameInd += 1
                    total_frame += 1

                elif key[pygame.K_KP_ENTER]:
                    image_array = np.vstack((image_array, temp_array))
                    label_array = np.vstack((label_array, direction[0]))
                    saved_frame += 1
                    frameInd += 1
                    total_frame += 1

                elif key[pygame.K_SPACE]:
                    image_array = np.vstack((image_array, temp_array))
                    label_array = np.vstack((label_array, direction[1]))
                    saved_frame += 1
                    frameInd += 1
                    total_frame += 1
            elif event.type == pygame.KEYUP:
                complex_cmd = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # save training images and labels
    train = image_array[1:, :]
    train_labels = label_array[1:, :]

    # save training data as a numpy file
    file_name = "trainingdata"
    directory = "training_data_npz"
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        np.savez(directory + '/' + file_name + '.npz', train=train, train_labels=train_labels)
    except IOError as e:
        print(e)
    time1 = cv2.getTickCount()
    # calculate streaming duration
    time = (time1 - time0) / cv2.getTickFrequency()
    print('Streaming duration: ', time)

    print(train.shape)
    print(train_labels.shape)
    print('Total frame: ', total_frame)
    print('Saved frame: ', saved_frame)
    print('Dropped frame: ', total_frame - saved_frame)
finally:
    print("EXIT")

cv2.destroyAllWindows()
vs.stop()
print(">>>>>Exit<<<<<")


















