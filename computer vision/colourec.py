# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import sys

import numpy as np
import cv2

#opencv2 uses BGR

#Order: Red, Orange, Green in HSV
colour = [ ([0,100,100],[10,255,255]) , ([10,150,150],[15,255,255]) , ([50,255,255],[70,255,255]) ]

#redup = np.array[0,0,255]
#reddown = np.array[0,0,150]

vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

font = cv2.FONT_HERSHEY_SIMPLEX
i=0
# loop over some frames...this time using the threaded stream
while(True):       
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        i= i + 1
        #print(frame)
        #print(type(frame))
        #print(frame.shape)
        #

        
        hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    
      #  frame = cv2.inRange(frame, redup, reddown)

        #Red
        redmask = cv2.inRange(hsvframe, np.array(colour[0][0]), np.array(colour[0][1])) #so in range tells us which pixels in our image fall into between the upper and lower bounds

        orangemask = cv2.inRange(hsvframe, np.array(colour[1][0]), np.array(colour[1][1])) #so in range tells us which pixels in our image fall into between the upper and lower bounds
 
        greenmask = cv2.inRange(hsvframe, np.array(colour[2][0]), np.array(colour[2][1])) #so in range tells us which pixels in our image fall into between the upper and lower bounds
 


##        print(type(mask))
##        print(mask)
##        nozero = cv2.findNonZero(mask)
##        print(nozero)
##        print(len(nozero))
        
        res = cv2.bitwise_and(frame,frame,mask=greenmask)
        
       # print(min(frame[1][1]))
        
       # cv2.putText(frame,"frame"+str(i), (50,50), font , 2, (255,255,255))
        cv2.imshow("Frame", res)
        
        # update the FPS counter
        fps.update()

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
 
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
