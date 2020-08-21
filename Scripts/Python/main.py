import cv2
import numpy as np
import math
import ctypes
from tracking import *
from streaming import *

stream = DataStream(create=True)
stream.settings.skin_tone = 255
stream.settings.skin_darker_than_background = True
stream.settings.samples = 20
stream.settings.sensivity = 100
#while stream.read == None: sleep(.2)


# Variables:

skin_tone                   = stream.settings.skin_tone
skin_darker_than_background = stream.settings.skin_darker_than_background
samples                     = stream.settings.samples
sensivity                   = stream.settings.sensivity

# __________


cap = cv2.VideoCapture(0)
cv2.namedWindow('Hand Tracking')
tracked = False
frames = 0
lowest = [0, 5, 20]
highest = [255, 150, 200]
user32 = ctypes.windll.user32


for i in range(40):
    frame = ReadFrame(cap, skin_darker_than_background)
    cv2.imshow('Hand Tracking', frame)
    k = cv2.waitKey(1)

screensize_multiplier = (
    user32.GetSystemMetrics(0) / frame.shape[0], 
    user32.GetSystemMetrics(1) / frame.shape[1]
)

tracking_area_l = (
    (0, int(frame.shape[1] /2)),        # x-line
    (0, int(frame.shape[0] /4 *3))      # y-line
)
tracking_area_r = (
    (int(frame.shape[1] /2), int(frame.shape[1]) -1),
    (0, int(frame.shape[0] /4 *3))
)

tracker_pos_l = (
    int(tracking_area_l[0][1] /2), 
    int((tracking_area_l[1][1] /2))
)
tracker_pos_r = (
    int(tracking_area_r[0][1] /4 *3), 
    int((tracking_area_r[1][1] /2))
)
print(frame.shape)

# Callibrate
while(1):
    frame = ReadFrame(cap, skin_darker_than_background)
    #frame, mask_l, mask_r = ImageProcessing(
    #    tracking_area_l, 
    #    tracking_area_r, 
    #    cap, 
    #    [
    #        lowest, 
    #        highest, 
    #        skin_tone
    #    ], 
    #    noisy_pixels_l, 
    #    noisy_pixels_r, 
    #    skin_darker_than_background
    #)

    index_x = tracker_pos_l[0]
    index_y = tracker_pos_l[1]
    col_l = GetAverageColorFromRegion(frame, (index_x, index_y), 10)
    
    index_x = tracker_pos_r[0]
    index_y = tracker_pos_r[1]
    col_r = GetAverageColorFromRegion(frame, (index_x, index_y), 10)
    print(f'{col_l}  |  {frame[index_x][index_y]}')
    score_l = (col_l[1] + col_l[2]) /2
    score_r = (col_r[1] + col_r[2]) /2

    result = f'{str(score_l)} | {str(frames)} | {str(len(color_values_l))}'
    cv2.putText(frame, result, (10,50), font, 2, ((0, 0, 255)), 3, cv2.LINE_AA)


    cv2.rectangle(frame,
        (
            tracking_area_l[0][0],
            tracking_area_l[1][0]
        ),
        (
            tracking_area_l[0][1] -2,
            tracking_area_l[1][1]
        ),
        (0,255,0), 4)

    cv2.rectangle(frame,
        (
            tracking_area_r[0][0] +2,
            tracking_area_r[1][0]
        ),
        (
            tracking_area_r[0][1],
            tracking_area_r[1][1]
        ),
        (255,0,0), 4)

    DrawTracker(frame, tracker_pos_l, score_l, len(color_values_l))
    DrawTracker(frame, tracker_pos_r, score_r, len(color_values_r))

    cv2.imshow('Hand Tracking',frame)
    frames += 1
    
    if score_l > skin_tone:
        if len(color_values_l) < samples: color_values_l.append(col_l)
    if score_r > skin_tone:
        if len(color_values_r) < samples: color_values_r.append(col_r)

    if score_l < skin_tone and score_r < skin_tone and len(color_values_l) >= samples and len(color_values_r) >= samples:
        
        for i in range(40):
            frame = ReadFrame(cap, skin_darker_than_background)

            cv2.imshow('Hand Tracking', frame)
            cv2.waitKey(1)
        
        frame, mask_l, mask_r = ImageProcessing(tracking_area_l, tracking_area_r, cap, [lowest, highest, skin_tone], noisy_pixels_l, noisy_pixels_r, skin_darker_than_background)

        for x in range(mask_l.shape[0]):
            for y in range(mask_l.shape[1]):
                if mask_l[x][y] > 200:
                    noisy_pixels_l.append((y, x))

        for x in range(mask_r.shape[0]):
            for y in range(mask_r.shape[1]):
                if mask_r[x][y] > 200:
                    noisy_pixels_r.append((y, x))
        
        break
        
    k = cv2.waitKey(1) & 0xFF
    if k == 27: break
    

for color in range(samples):
    for channel in range(3):
        if color_values_l[color][channel] > highest[channel]: highest[channel] = color_values_l[color][channel]
        if color_values_l[color][channel] < int(lowest[channel] *sensivity): lowest[channel] = int(color_values_l[color][channel] /sensivity)
lowest = [0, 5, 20]
highest = [255, 150, 200]
print(score_l)
print(score_r)
print(lowest)
print(highest)
total = frame.shape[0] * frame.shape[1]
part = len(noisy_pixels_l) + len(noisy_pixels_r)
percentage = 100 * part / total
print(percentage)
if (percentage > 100):
    print('Please use a darker background')
    exit()
#cv2.destroyAllWindows()

while(1):
    #try:  #an error comes if it does not find anything in window as it cannot find contour of max area
          #therefore this try error statement
          
        frame, mask_l, mask_r = ImageProcessing(tracking_area_l, tracking_area_r, cap, [lowest, highest, skin_tone], noisy_pixels_l, noisy_pixels_r, skin_darker_than_background)
        if skin_darker_than_background: frame = 255 - frame

        roi_l=frame[
            tracking_area_l[0][0]:tracking_area_l[0][1],
            tracking_area_l[1][0]:tracking_area_l[1][1]
        ]
        roi_r=frame[
            tracking_area_r[0][0]:tracking_area_r[0][1],
            tracking_area_r[1][0]:tracking_area_r[1][1]
        ]

        cv2.rectangle(frame,(tracking_area_l[1][0],tracking_area_l[0][0]),(tracking_area_l[1][1],tracking_area_l[0][1]),(0,255,0),0)    
        cv2.rectangle(frame,(tracking_area_r[1][0],tracking_area_r[0][0]),(tracking_area_r[1][1] -1,tracking_area_r[0][1]),(0,255,0),0)    
        hsv_l = cv2.cvtColor(roi_l, cv2.COLOR_BGR2HSV)
        hsv_r = cv2.cvtColor(roi_r, cv2.COLOR_BGR2HSV)
    
        try:
            pos_l = HandTracking(frame, mask_l, roi_l)
            pos_r = HandTracking(frame, mask_r, roi_r)
            hand_positions = [pos_l, (pos_r[0] + tracking_area_l[1][1], pos_r[1])]
            cv2.putText(frame,str(hand_positions),(100,50), font, 1, ((0, 0, 255)), 1, cv2.LINE_AA)
            #print(hand_positions)
            translated = (int(pos_l[0] * screensize_multiplier[0]), int(pos_l[1] * screensize_multiplier[1]))
            print("t" + str(translated))
            stream.hand_l_pos_x = pos_l[0]
            stream.hand_l_pos_y = pos_l[1]
            stream.hand_r_pos_x = pos_r[0]
            stream.hand_r_pos_y = pos_r[0]
            #moveTo(translated)
        except Exception as e: print('Exeption: ' + str(e))

        #show the windows
        masks = np.concatenate((mask_l, mask_r), axis=1)
        cv2.imshow('masks',masks)
        if skin_darker_than_background: frame = 255 - frame
        cv2.imshow('Hand Tracking',frame)

        if not tracked:
            print('got track again...')
            tracked = True

            
        if False:
            cv2.putText(frame,'Completely lost track!',(10,50), font, 2, ((0, 0, 255)), 3, cv2.LINE_AA)
            cv2.imshow('Hand Tracking',frame)
            tracked = False
            pass
        
    
        #CheckForRequest()

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    
cv2.destroyAllWindows()
cap.release()    
    



'''
frame_l = cap.read()
    frame_l=cv2.flip(frame_l,1)

    kernel = np.ones((3,3),np.uint8)
    
#define region of interest
    roi=frame_l[
        tracking_area_l[0][0]:tracking_area_l[0][1],
        tracking_area_l[1][0]:tracking_area_l[1][1]
    ]
    
    
    cv2.rectangle(frame_l,(tracking_area_l[1][0],tracking_area_l[0][0]),(tracking_area_l[1][1],tracking_area_l[0][1]),(0,255,0),0)    
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    
     
# define range of skin color in HSV
    lower_skin = np.array(lowest, dtype=np.uint8)
    upper_skin = np.array(highest, dtype=np.uint8)
    
 #extract skin colur imagw  
    mask_l = cv2.inRange(hsv, lower_skin, upper_skin)
    

    
#extrapolate the hand to fill dark spots within
    mask_l = cv2.dilate(mask_l,kernel,iterations = 4)
    
#blur the image
    mask_l = cv2.GaussianBlur(mask_l,(5,5),100) 
    
#invert mask_l for white skin
    if skin_tone >= 100: mask_l = (255 - mask_l)
    
'''