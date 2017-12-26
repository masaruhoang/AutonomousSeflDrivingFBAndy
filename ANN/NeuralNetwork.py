import cv2


class NeuralNetwork:
    def __init__(self):
        '''
        Ex: self.model = cv2.ml.ANN_MLP_load("D:/AutonomousDrivingAndy/weightXML/weightXML.xml")
        '''
        self.model = cv2.ml.ANN_MLP_load("YOUR_PATH")

    def predict(self, frame):
        ret, resp = self.model.predict(frame)
        return resp.argmax(-1)

