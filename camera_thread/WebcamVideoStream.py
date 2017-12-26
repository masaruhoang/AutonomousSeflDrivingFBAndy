
from threading import Thread
import cv2

class WebcamVideoStream:
    def __init__(self, src = 0):
        '''
            initialize the video camera srteam and read the first frame
            from the stream
        '''
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        
        ''' 
            initialize the variable used to indicate the thread should 
            bes stopped
        '''
        self.stopped = False
        
    def start(self):
        '''Start the thread to read frames from the  video stream'''
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        ''' Keep looping infinitely until the thread is stopped'''
        while True:
            ''' If the thread indicator variable is set, stop the thread'''
            if self.stopped:
                return
            
            ''' Otherwise, read the next frame from the stream'''
            (self.grapped, self.frame) = self.stream.read()
           
    def read(self):
        ''' Return the frame the most recently read'''
        return self.frame
    
    def stop(self):
        ''' Indicate that the thread should be stopped'''
        self.stopped = True
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
