#Mee, Punna, Porsche
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

control_pinsY = [40,38,36,32]
control_pinsX = [15,11,13,12]
screenwidth = 640
screenheight = 480

for pin in control_pinsX:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
for pin2 in control_pinsY:
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.output(pin2, 0)
halfstep_seqL = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
    
]
halfstep_seqR = [
    [1,0,0,1],
    [0,0,0,1],
    [0,0,1,1],
    [0,0,1,0],
    [0,1,1,0],
    [0,1,0,0],
    [1,1,0,0],
    [1,0,0,0]
    
]




face_cascade = cv2.CascadeClassifier('/home/pi/Pictures/data/haarcascade_frontalface_default.xml')

camera = PiCamera()
camera.rotation =270
camera.resolution = (640, 480)
camera.framerate = 24

rawCapture = PiRGBArray(camera, size = (screenwidth, screenheight))



time.sleep(1)
    
try: 
    for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
        img = frame.array
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        stack = []
        

        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            xmid = (screenwidth-(w))/2
            ymid = (screenheight-h)/2
            

            if x<xmid-50:
                
                for i in range(1):
                    for halfstep in range(8):
                        for pin in range(4):
                            GPIO.output(control_pinsX[pin], halfstep_seqL[halfstep][pin])
                        time.sleep(0.01)

                print("movv left")
                time.sleep(0.1)
                
            elif x>xmid+50:
                print("movv right")
                
                for i in range(1):
                    for halfstep in range(8):
                        for pin in range(4):
                            GPIO.output(control_pinsX[pin], halfstep_seqR[halfstep][pin])
                        time.sleep(0.01)
                time.sleep(0.1)
                
            
            if y>ymid+30:
                print("movv down")
                
                for i in range(1):
                    for halfstep in range(8):
                        for pin2 in range(4):
                            GPIO.output(control_pinsY[pin2], halfstep_seqL[halfstep][pin2])
                        time.sleep(0.01)
                time.sleep(0.1)
                
            elif y<ymid-30:
                print("movv up")
                
                for i in range(1):
                    for halfstep in range(8):
                        for pin2 in range(4):
                            GPIO.output(control_pinsY[pin2], halfstep_seqR[halfstep][pin2])
                        time.sleep(0.01)
                time.sleep(0.1)
                
            
            break
        
        
        
        cv2.imshow("Frame", img)
        
        key = cv2.waitKey(1)
        
        rawCapture.truncate(0)
            
        if key == ord("q"):
            break
finally:
    cv2.destroyAllWindows()
    GPIO.cleanup()
    print("done")
