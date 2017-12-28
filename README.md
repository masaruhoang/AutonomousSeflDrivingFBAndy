# Self Driving Firebase Andy Robot
## AndroidThingsAndyRobot
## Dwayne Hoang
## OpenCV, Machine Learning
## Java, Kotlin, Python
## MY BLOG: https://andpythings.wordpress.com

# Introduction
Andy Robot still used in this project, it could can self-driving on the track and detecting Stop Sign with stop for 5s.
###### Android-Things (Andy Robot)
- Raspeberry Pi3  Model B
###### Computer
- Supervised Learning with ANN (Artificial Neural Network).
- Using MLP (Mutil-Layer Perceptrons )  in  OpenCV 3.3.0.1.
- Object Detection (Haar feature-based cascade classifiers).
- Written in Python 3.6
- Firebase Realtime Database.
###### Camera
- Camera Stream from any Smartphone which be able to connect Wifi (LAN)
# Tools
- Android Studio 3 ( For Android-Things)
- Pycharm 2017.3.1 (For Python, Opencv, ANN)
- DroidCamApp (both of SmartPhone and Computer)
# Python 3.6 Libraries
- numpy, pygame,, imutils
- cv2 (OpenCV 3.3.0.1)
- pyrebase (latest version)
# System Design
![Alt text](https://andpythings.files.wordpress.com/2017/12/system-design.png")
# Functions
- **ANN folder** : Contain Init Neural Network class.
- **camera_thread folder** : Contain Init and methods using run camera in Background thread to avoid block Main thread.
- **cascade_xml folder** : Trained cascade classifiers xml files.
- **firebase folder** : Use to config authenticate a user who want to connect to Firebase.
- **dataset_images folder** : Collected Image Will Be Saved Here.
- **firebaseAdminKey folder** : Firebase_Admin_API_KEY.json Will Be Saved Here.
- **objectDetection folder** : trained stop sign classifiers are included in the “cascade_xml” folder.
- **training_data_npz folder** : TraingData.npz Will Be Saved Here.
- **weightXML folder** : WeightXML.xml Will Be Saved Here.
 

- **collecting_data.py** —>  Collecting images that get used to traning by user must get  them annually (Using keyboard to control Robot). Images data is saved as a npz file in training_data_npz folder
- **ann_trainer.py** —> When we fully have npz file, start training dataset and model    which will be saved such as weightxml.xml in weightXML folder.
- **camera_main.py** —> Prediction dely on trained dataset and give results. Then, send that results to Firebase

## Thank AutoRCCar – hamuchiwa so much for detail tutorial on the blog and code to refer.
