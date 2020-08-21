import cv2
import numpy as np
import math

global roi
global color_values_l
global color_values_r
global noisy_pixels_l
global noisy_pixels_r
global hand_positions
color_values_l = []
color_values_r = []
noisy_pixels_l = []
noisy_pixels_r = []
font = cv2.FONT_HERSHEY_SIMPLEX

def ReadFrame(cap, invert = False):
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)
    if invert: frame = 255 - frame

    return frame

def GetAverageColorFromRegion(frame, position, region_size):
    colors = []
    average_color = [0, 0, 0]

    for x in range(region_size):
        for y in range(region_size):
            try:
                color = frame[position[0] + x][position[1]]
                colors.append(color)
            except:
                pass

            try:
                color = frame[position[0] - x][position[1]]
                colors.append(color)
            except:
                pass

            try:
                color = frame[position[0]][position[1] + y]
                colors.append(color)
            except:
                pass

            try:
                color = frame[position[0]][position[1] - y]
                colors.append(color)
            except:
                pass

    for color in colors:
        average_color[0] += color[0]
        average_color[1] += color[1]
        average_color[2] += color[2]

    average_color[0] /= len(colors)
    average_color[1] /= len(colors)
    average_color[2] /= len(colors)
    average_color[0] = int(average_color[0])
    average_color[1] = int(average_color[1])
    average_color[2] = int(average_color[2])

    return average_color

def DrawTracker(frame, position, score, samples):
    cv2.ellipse(
        frame, 
        position, 
        (samples +20, samples +20), 0, -90, 
        (score /255 *360), 
        [0, score, 255 - score], 
        -1
    )

    cv2.ellipse(
        frame, 
        position, 
        (samples +20, samples +20), 0, -90, 
        (score /255 *360), 
        [100, 200, 200], 
        2
    )

def ImageProcessing(tracking_area_l, tracking_area_r, cap, skin_colors, noisy_pixels_l, noisy_pixels_r, skin_darker_than_background):
    frame = ReadFrame(cap, skin_darker_than_background)
    
    kernel = np.ones((3,3),np.uint8)
    
#define region of interest
    roi_l=frame[
        tracking_area_l[0][0]:tracking_area_l[0][1],
        tracking_area_l[1][0]:tracking_area_l[1][1]
    ]
    roi_r=frame[
        tracking_area_r[0][0]:tracking_area_r[0][1],
        tracking_area_r[1][0]:tracking_area_r[1][1]
    ]
    
    hsv_l = cv2.cvtColor(roi_l, cv2.COLOR_BGR2HSV)
    hsv_r = cv2.cvtColor(roi_r, cv2.COLOR_BGR2HSV)
    
    
     
# define range of skin color in HSV
    lower_skin = np.array(skin_colors[0], dtype=np.uint8)
    upper_skin = np.array(skin_colors[1], dtype=np.uint8)
    
 #extract skin colur imagw  
    mask_l = cv2.inRange(hsv_l, lower_skin, upper_skin)
    mask_r = cv2.inRange(hsv_r, lower_skin, upper_skin)
    

    
#extrapolate the hand to fill dark spots within
    mask_l = cv2.dilate(mask_l,kernel,iterations = 4)
    mask_r = cv2.dilate(mask_r,kernel,iterations = 4)
    
#blur the image
    mask_l = cv2.GaussianBlur(mask_l,(5,5),100) 
    mask_r = cv2.GaussianBlur(mask_r,(5,5),100) 
    
#invert mask for white skin
    if skin_colors[2] >= 100:
        mask_l = (255 - mask_l)
        mask_r = (255 - mask_r)

#remove noise
    for pixel in noisy_pixels_l:
        cv2.circle(mask_l, pixel, 50, 255, -1)
        #mask_l[pixel[0], pixel[1]] = (255, 255, 255)

    for pixel in noisy_pixels_r:
        cv2.circle(mask_r, pixel, 50, 255, -1)

    return frame, mask_l, mask_r


def HandTracking(frame, mask, roi):
#find contours
    contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#find contour of max area(hand)
    cnt = max(contours, key = lambda x: cv2.contourArea(x))
    
#approx the contour a little
    epsilon = 0.0005*cv2.arcLength(cnt,True)
    approx= cv2.approxPolyDP(cnt,epsilon,True)
   
    
#make convex hull around hand
    hull = cv2.convexHull(cnt)
    
 #define area of hull and area of hand
    areahull = cv2.contourArea(hull)
    areacnt = cv2.contourArea(cnt)
  
#find the percentage of area not covered by hand in convex hull
    arearatio=((areahull-areacnt)/areacnt)*100

 #find the defects in convex hull with respect to hand
    hull = cv2.convexHull(approx, returnPoints=False)
    defects = cv2.convexityDefects(approx, hull)
    
# l = no. of defects
    l=0
    
#code for finding no. of defects due to fingers
    lowest_point = (frame.shape[0], frame.shape[1])

    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(approx[s][0])
        end = tuple(approx[e][0])
        far = tuple(approx[f][0])
        pt= (100,180)
        
        
        #find length of all sides of triangle
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        s = (a+b+c)/2
        ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
        
        #distance between point and convex hull
        d=(2*ar)/a
        
        #apply cosine rule here
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        
    
        #ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
        if angle <= 90 and d>30:
            l += 1
            cv2.circle(roi, far, 3, [255,0,0], -1)
        
        #draw lines around hand
        cv2.line(roi,start, end, [0,255,0], 2)

        #check for highest point
        if start[1] < lowest_point[1]: lowest_point = start
        if end[1] < lowest_point[1]: lowest_point = end
        
    cv2.circle(roi, lowest_point, 10, [0,255,0], -1)

    l+=1

    
    #print corresponding gestures which are in their ranges
    if l==1:
        if areacnt<2000:
            cv2.putText(frame,'Put hand in the box',(0,20), font, 1, ((0, 100, 200)), 1, cv2.LINE_AA)
        else:
            if arearatio<12:
                cv2.putText(frame,'0',(0,20), font, 1, (((100, 200, 0))), 1, cv2.LINE_AA)
            elif arearatio<17.5:
                cv2.putText(frame,'Best of luck',(0,20), font, 1, (((100, 200, 0))), 1, cv2.LINE_AA)
               
            else:
                cv2.putText(frame,'1',(0,20), font, 1, (((100, 200, 0))), 1, cv2.LINE_AA)
                
    elif l==2:
        cv2.putText(frame,'2',(0,20), font, 1, (((100, 200, 0))), 1, cv2.LINE_AA)
        
    elif l==3:
     
          if arearatio<27:
                cv2.putText(frame,'3',(0,20), font, 1, (((100, 200, 0))), 1, cv2.LINE_AA)
          else:
                cv2.putText(frame,'3',(0,20), font, 1, (((100, 200, 0))), 1, cv2.LINE_AA)
                
    elif l==4:
        cv2.putText(frame,'4',(0,20), font, 1, (((100, 200, 0))), 1, cv2.LINE_AA)
        
    elif l==5:
        cv2.putText(frame,'5',(0,20), font, 1, (((100, 200, 0))), 1, cv2.LINE_AA)
        
    elif l==6:
        cv2.putText(frame,'reposition',(0,20), font, 1, (((100, 200, 0))), 1, cv2.LINE_AA)
        
    else:
        cv2.putText(frame,'reposition',(10,50), font, 1, (((100, 200, 0))), 1, cv2.LINE_AA)

    return lowest_point