##### Suggested clean drone startup sequence #####
import time, sys
import ps_drone                                    # Import PS-Drone-API
import cv2
from numba import njit # for faster compilation
from PIL import Image
import numpy as np
import skimage.measure
def rule2(pixel):
    return pixel[2]>100
@njit(fastmath=True)#float64(int32, int32)
def rule(pixel):
    #converting to HSV
    min_val = min(pixel)
    max_val = max(pixel)
    if  max_val - min_val< 30: #gray or dark or too bright
         return False
    d = (int(pixel[1])-pixel[0]) if (pixel[2]==min_val) else ((int(pixel[2])-pixel[1]) if (pixel[0]==min_val) else (int(pixel[0])-pixel[2]))
    h = 3 if (pixel[2]==min_val) else (1 if (pixel[0]==min_val) else 5)
    H = (h - float(d)/(max_val-min_val))
    S = float(max_val - min_val)/max_val
    #S_simpl = (max_val - min_val)
    return (H < 0.5 or H>5.5) and (S>0.7) and (max_val > 55);
    #and S > 0.4 and max_val > 80

    
@njit(fastmath=True)
def countSums(image):
    sum1 =0
    sum2 =0
    sum_all = 0
    width, height,_= image.shape
    for i in range(0,int(height/2)):
        for j in range(0,int(width/2)):
            temp = image[j,i]
            if rule(temp):#and rule(image[i,max(0,j-1)]):
                sum1+=1
                sum2+=1
                sum_all+=1
                image[j,i] = [255,255,255]
            else:
                image[j,i] = [0,0,0]
        for j in range(int(width/2),width) :
            temp = image[j,i]
            if rule(temp):# and rule(image[i,max(0,j-1)]):
                sum1+=1
                sum2-=1
                sum_all+=1;
                image[j,i] = [255,255,255]
            else:
                image[j,i] = [0,0,0]
    for i in range(int(height/2),height):
        for j in range(0,int(width/2)):
            temp = image[j,i]
            if rule(temp):# and rule(image[i,max(0,j-1)]):
                sum1-=1
                sum2+=1
                sum_all+=1;
                image[j,i] = [255,255,255]
            else:
                image[j,i] = [0,0,0]
        for j in range(int(width/2),width):
            temp = image[j,i]
            if rule(temp):# and rule(image[i,max(0,j-1)]):
                sum1-=1
                sum2-=1
                sum_all+=1;
                image[j,i] = [255,255,255]
            else:
                image[j,i] = [0,0,0]
    
    
    #cv2.waitKey(0)
    #drone.stopVideo()
    return sum1,sum2,sum_all # x,y

@njit(fastmath=True)
def getSquare(image):
    width, height,_= image.shape
    left =width
    right =-1
    top = height
    bottom = -1

    for i in range(0,int(height)):
        for j in range(0,int(width)):
            temp = image[j,i]
            if rule(temp):
                if j < left:
                    right = j;
                elif j > right:
                    right = j;
                if i < top:
                    top = i;
                if i > bottom:
                    bottom = j;  
    #cv2.waitKey(0)
    #drone.stopVideo()
    return left, right, top, bottom # x,y

def filter_dots(image,lambd):
    image2 = image.copy()
    for i in range(len(image)):
        for j in range(len(image[i])):
            image2[i,j] = lambd(np.array((image[i,j],image[max(0,i-1),j],image[i,max(0,j-1)],image[min(i+1,len(image)-1), j], image[i, min(j+1,len(image[i])-1)])))
    return image2
image = Image.open("test.png")
imaged = np.array(image)
imaged = cv2.cvtColor(imaged, cv2.COLOR_BGR2RGB)
#cv2.imshow('image',imaged)
#cv2.waitKey()
def true_min(arr):
    val = min(arr[:,0])
    return [val,val,arr[0,2]];

print(type(imaged))
countSums(imaged)
imaged = filter_dots(imaged,true_min)
imaged = filter_dots(imaged,true_min)
imaged = filter_dots(imaged,true_min)
image = Image.fromarray(imaged)
image.save("test_processed.png")
print("counted!")
drone = ps_drone.Drone()                           # Start using drone
drone.startup()                                    # Connects to drone and starts subprocesses
drone.reset()                                      # Sets drone's status to good
while (drone.getBattery()[0]==-1): time.sleep(0.1) # Wait until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"% "+str(drone.getBattery()[1]) # Battery-status
drone.useDemoMode(True)                            # Set 15 basic dataset/sec

##### Mainprogram begin #####
drone.setConfigAllID()                              # Go to multiconfiguration-mode
drone.sdVideo()                                     # Choose lower resolution (try hdVideo())
drone.frontCam()                                    # Choose front view
CDC = drone.ConfigDataCount
while CDC==drone.ConfigDataCount: time.sleep(0.001) # Wait until it is done (after resync)

drone.videoFPS(30)
drone.videoBitrate(9000)
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
stop =   False

# define vieo recording
#recorder = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc(*"MJPG"),10,(int(320),int(240)))
curTime = time.time()
#drone.takeoff();
#time.sleep(5);
#drone.moveUp(0.8);
#time.sleep(5);
#drone.moveUp(0);

while not stop:
    while drone.VideoImageCount==IMC: time.sleep(0.01) # Wait until the next video-frame
    IMC = drone.VideoImageCount
    key = drone.getKey()
    #curTime = time.time()
    sumx, sumy, sum_all =  countSums(drone.VideoImage)
    left ,right, top, bottom = getSquare(drone.VideoImage)
    width, height, _  = drone.VideoImage.shape
    center_2x = (left+right)/width
    center_2y = (top + bottom)/height
    cv2.imshow('image',drone.VideoImage)
    #cv2.imshow('image',cv2.rectangle(drone.VideoImage,(left,top),(right,bottom),color=(0,255,0),thickness = 3))

    #recorder.write(drone.VideoImage)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.stopVideo()
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
    '''
    if sumx >500:
        #drone.turnLeft(1)
        right  = -0.4
        #drone.turnAngle(-15, 0.8);
        #drone.moveLeft(0.1)
        print "left "+str(sumx) #
    elif sumx < -500:
        right = 0.4
        #drone.turnRight(1)
        #drone.turnAngle(15, 0.8);
        #drone.moveRight(0.1)
        print "right "+str(sumx) #
    else:
        right = 0
        #drone.moveLeft(0);
    
    if sumy > 100:
        #forward = 0.2;
        drone.moveForward(0.1)
        print "forward "+str(sumy) #
    elif sumy < -100:
        drone.moveBackward(0.1)
        print "backward "+str(sumy) #
    else:
        drone.moveForward(0);
    
    if sum_all > 4000:
        forward = 0.1;#-0.2;
    elif sum_all > 500:
        forward =0.04
    else:
        forward = 0;
    '''
    print (forward,right)
    if key == "w":
        print("w")
        drone.move(0,forward,0,right); ### FIXED ### ((time.time() - curTime)%1)-0.5
    else:
        drone.stop()
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