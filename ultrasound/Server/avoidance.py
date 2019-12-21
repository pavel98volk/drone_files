import time, sys
import ps_drone                                    # Import PS-Drone-API
import cv2
from numba import njit # for faster compilation
import socket
import numpy as np
import threading

UDP_IP = "192.168.1.1"
UDP_PORT = 9123
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE
  
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT)) # STRANGE THINGS MADE ME DISCOVER THIS is much needed

data = []
def get_values():
    global data
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        #print "received message:", ord(data[0]),ord(data[1]),ord(data[2]), ord(data[3])

datathread = threading.Thread(target=get_values,args=(1,))
datathread.start()




drone = ps_drone.Drone()                           # Start using drone
drone.startup()                                    # Connects to drone and starts subprocesses
drone.reset()                                      # Sets drone's status to good
while (drone.getBattery()[0]==-1): time.sleep(0.1) # Wait until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"% "+str(drone.getBattery()[1]) # Battery-status
##### Mainprogram begin #####
drone.setConfigAllID()                              # Go to multiconfiguration-mode
drone.sdVideo()                                     # Choose lower resolution (try hdVideo())
drone.frontCam()                                    # Choose front view
CDC = drone.ConfigDataCount
while CDC==drone.ConfigDataCount: time.sleep(0.001) # Wait until it is done (after resync)

drone.videoFPS(30)
drone.videoBitrate(6000)
drone.fastVideo(True)#false
#drone.groundVideo(True) 

drone.startVideo() 
                                 # Start video-function
#drone.showVideo()                                   # Display the video

##### And action !
print "Use to toggle front- and cdgroundcamera, any other key to stop"
IMC =    drone.VideoImageCount # Number of encoded videoframes
stop =   False
ground = False
# define vieo recording
#recorder = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc(*"MJPG"),10,(int(320),int(240)))
curTime = time.time()
drone.takeoff();
#time.sleep(2);
#drone.moveUp(0.8);
#time.sleep(5);
#drone.moveUp(0);

while not stop:
    while drone.VideoImageCount==IMC: time.sleep(0.01) # Wait until the next video-frame
    IMC = drone.VideoImageCount
    key = drone.getKey()
    
    #cv2.imshow('image',drone.VideoImage)
    #recorder.write(drone.VideoImage)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #drone.stopVideo()
    #print(time.time() - curTime)
    #drone.doggyWag()
    '''
    print(type(drone.VideoImage))
    print(type(drone.VideoImage[0]))
    print(type(drone.VideoImage[0][0]))
    print(type(drone.VideoImage[0][0][0]))
    print('----------')
    '''
    # for topdown camera
    right = 0;
    forward =0;
    if key =="d":
        #drone.turnLeft(1)
        right  = 0.5
        #drone.turnAngle(-15, 0.8);
        #drone.moveLeft(0.1)
        #print "left "+str(sumx) #
    elif key =="a":
        right = -0.5
        #drone.turnRight(1)
        #drone.turnAngle(15, 0.8);
        #drone.moveRight(0.1)
        #print "right "+str(sumx) #
    else:
        right = 0
        #drone.moveLeft(0);
    '''
    if sumy > 100:
        #forward = 0.2;
        drone.moveForward(0.1)
        print "forward "+str(sumy) #
    elif sumy < -100:
        drone.moveBackward(0.1)
        print "backward "+str(sumy) #
    else:
        drone.moveForward(0);
    '''
    if key == "w":
        forward = 0.1;#-0.2;
    elif key == "s":
        forward =-0.1
    else:
        forward = 0;

    if (((forward !=0) or (right !=0)) and min(data[0],data[1],data[2])>100):
        drone.relMove(0,forward,0,right,0,0.001); ### FIXED ### ((time.time() - curTime)%1)-0.5
    else:
        drone.hover();

    if time.time() - curTime > 30:
        #drone.land()
        pass
    
    if key==" ":
        #recorder.release()
        drone.land()
        stop = True

    '''
        if ground:    ground = False
        else:         ground = True
        drone.groundVideo(ground)                    # Toggle between front- and groundcamera.
    elif key and key != " ": stop = True 
    '''