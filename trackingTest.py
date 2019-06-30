import numpy as np
import cv2

#cap = cv2.VideoCapture(1) #0 for computer cam, 1 for connected USB cam
cap = cv2.imread('C:/Users/wruet/Pictures/Camera Roll/WIN_20190627_16_56_18_Pro.jpg') #for still image

length = cv2.CAP_PROP_FRAME_HEIGHT
width = cv2.CAP_PROP_FRAME_WIDTH
maskValMin = np.array([80,90,75]) #minimum HSV values for thresholding
maskValMax = np.array([100,255,255]) #maximum HSV values for thresholding

#cap.set(length, 1280) #set length of cap
#cap.set(width, 720) #set width of cap

while(True):
    #ret, frame = cap.read() #sets frame equal to the video capture
    frame = cap #for still image, because I don't feel like changing everywhere it says 'frame'

    colorImg = cv2.cvtColor(frame, cv2.IMREAD_COLOR) #BGR version of cap
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #HSV version of cap, used for thresholding
    mask = cv2.inRange(hsv, maskValMin, maskValMax) #returns array of pixels within thresholding values
    final = frame #for still image - prevents original image from being altered

    final = cv2.bitwise_and(frame, final, mask = mask) #removes all pixels that aren't within thresholding range from final image
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finds contours from the binary image returned by cv2.inRange
    cv2.drawContours(final, contours, -1, (255, 0, 0), 3) #draws contours on final image

    if len(contours) > 1: #prevents errors I think. Maybe not idk
        contoursSorted = sorted(contours, key=cv2.contourArea, reverse=True) #sorts contours largest -> smallest
        cntMax = contoursSorted[0] #largest contour
        cnt2 = contoursSorted[1] #second largest contour
        cntTogether = [] #empty for later use

        #Find Bounding Rectangle Values-------------------------------------------------------
        cntTog = contoursSorted[0], contoursSorted[1] #combines largest and second largest contours
        for c in cntTog: #for each contour in cntTog
            x,y,w,h = cv2.boundingRect(c) #assigns the origin x/y values, width and height of each contour to x, y, w, h
            cntTogether.append([x,y,x+w,y+h]) #combines all of the values above into one list
        x, y, w, h = cv2.boundingRect(cntMax) 
        x2, y2, w2, h2 = cv2.boundingRect(cnt2)
        cntTogether = np.asarray(cntTogether) #converts cntTogether into an array
        left = np.min(cntTogether[:,0]) #sorts column 1 of array 'cntTogether' for minimum x value
        top = np.min(cntTogether[:,1]) #sorts column 2 of array 'cntTogether' for minimum y value
        right = np.max(cntTogether[:,2]) #sorts column 3 of array 'cntTogether' for maximum x value
        bottom = np.max(cntTogether[:,3]) #sorts column 4 of array 'cntTogether' for maximum y value
        #these are the four points needed to draw the rectangle around the two targets
        #--------------------------------------------------------------------------------------

        #Find Center of Bounding Rectangle----------------------------------------------------
        centerx = str(right - left) # finds center x value of rectangle
        centery = str(bottom-top) #finds center y value of rectangle
        #--------------------------------------------------------------------------------------

        #Draw Rectangles and Text-------------------------------------------------------------
        cv2.rectangle(final,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.rectangle(final,(x2,y2),(x2+w2,y2+h2),(0,0,255),2)
        cv2.rectangle(final,(left,top),(right,bottom),(255,0,0),2)
        cv2.putText(final, 'Center: ' + centerx + ", " + centery, (0,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        #--------------------------------------------------------------------------------------
        

    cv2.imshow('frame', final) #show final image, shockingly

    if cv2.waitKey(1) & 0xFF == ord('q'): #if Q key is pressed, exit the loop, thereby releasing cap and closing windows
        break

#cap.release()
cv2.destroyAllWindows() #closes all windows