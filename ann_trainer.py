import cv2
import numpy as np
import glob
import sys
from sklearn.model_selection import train_test_split

'''*******************INIT***********************'''
time0 = cv2.getTickCount()

# Load Training Data
image_array = np.zeros((1, 38400))
label_array = np.zeros((1, 3), 'float')
training_data = glob.glob('training_data_npz/*.npz')
print('Training Data be Loading....')

# If There is no data -> Exit
if not training_data:
    print("There is no training data in Directory. Please collect data before training data.")
    sys.exit()

for single_npz in training_data:
    with np.load(single_npz) as data:
        train_temp = data['train']
        train_labels_temp = data['train_labels']

    image_array = np.vstack((image_array, train_temp))
    label_array = np.vstack((label_array, train_labels_temp))

X = image_array[1:, :]
y = label_array[1:, :]
print ('Image array shape: ', X.shape)
print ('Label array shape: ', y.shape)


time1 = cv2.getTickCount()
time = (time1 - time0) / cv2.getTickFrequency()
print('Loading image duration:', time)

# train test split, 7:3
train, test, train_labels, test_labels = train_test_split(X, y, test_size=0.3)

# set start time
time3 = cv2.getTickCount()

# create MLP
layer_sizes = np.int32([38400, 32, 3])
model = cv2.ml.ANN_MLP_create()
model.setLayerSizes(layer_sizes)
model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
model.setBackpropMomentumScale(0.0)
model.setBackpropWeightScale(0.001)
model.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 20, 0.01))
model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 2, 1)

print('Training ...')
num_iter = model.train(np.float32(train), cv2.ml.ROW_SAMPLE, np.float32(train_labels))

# set end time
time4 = cv2.getTickCount()
timeN = (time4 - time3)/cv2.getTickFrequency()
print ('Training duration:', time)

# train data
ret_0, resp_0 = model.predict(train)
prediction_0 = resp_0.argmax(-1)
true_labels_0 = train_labels.argmax(-1)

train_rate = np.mean(prediction_0 == true_labels_0)
print ('Train accuracy: ', "{0:.2f}%".format(train_rate * 100))

# test data
ret_1, resp_1 = model.predict(test)
prediction_1 = resp_1.argmax(-1)
true_labels_1 = test_labels.argmax(-1)

test_rate = np.mean(prediction_1 == true_labels_1)
print ('Test accuracy: ', "{0:.2f}%".format(test_rate * 100))

# save model
model.save('weightXML/weightXML.xml')
print(model.isTrained())



