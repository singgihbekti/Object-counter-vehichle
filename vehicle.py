# -*- coding: utf-8 -*-
"""
Created on Fri May 28 21:29:49 2021

@author: Singgih
"""

import cv2
import csv 
import datetime as DT
import time

# Method 2
vidCap = cv2.VideoCapture('C:/Users/Singgih/Downloads/Compressed/vehicle counting -20210525T190033Z-001/vehicle counting/video.mp4')

# initilize OpenCV - Background Subtractor for KNN and MOG2
BS_KNN = cv2.createBackgroundSubtractorKNN()
BS_MOG2 = cv2.createBackgroundSubtractorMOG2()

vehile = 0
vehicle_kiri=0
vehicle_kanan=0
validVehiles = []

hr=[]
vki=[]
vka=[]
vto=[]

while vidCap.isOpened():
    now= DT.datetime.now() #date-time
    ret, frame = vidCap.read() # reads the next frame

    # extract the foreground mask
    fgMask = BS_MOG2.apply(frame)
    
    # draw the reference traffic lines 
    cv2.line(frame, (220,450), (1000,450), (0,0,255), 2) # RED Line kiri= 220-600; kanan= 680-1000
    cv2.line(frame, (220,440), (1000,440), (0,255,0), 1) # GREEN Offset ABOVE
    cv2.line(frame, (220,460), (1000,460), (0,255,0), 1) # GREEN Offset BELOW
    
    # extract the contours
    conts, _ = cv2.findContours(fgMask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in conts:
        x, y, w, h = cv2.boundingRect(c)
        
        # ignore the small contours in size
        visibleVehile = (w > 60) and (h > 60)
        if not visibleVehile:
            continue
        
        # remove the distraction on the road; consider only the objects on ROAD
        if x > 250 and x < 900 and y > 200:
            # draw the bounding rectangle for all contours
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            xMid = int((x + (x+w))/2)
            yMid = int((y + (y+h))/2)
            cv2.circle(frame, (xMid,yMid),5,(0,0,255),5)

            # add all valid vehiles into List Array
            validVehiles.append((xMid,yMid))
#             cv2.waitKey(0) # debugging purpose
            
            # saatnya ngitung kendaraan ===========================================================================
            # saatnya ngitung kendaraan ================================================total
            for (vX, vY) in validVehiles:
                if vY > 450 and vY < 456: # adjust this for the frame jumping
                        vehile += 1
                        #validVehiles.remove((vX,vY))
                        vto.append(vehile)

            # saatnya ngitung kendaraan =========================================kiri
            #for (vX, vY) in validVehiles:
                if vY > 450 and vY < 456: # adjust this for the frame jumping
                    if vX >200 and vX <600:
                        vehicle_kiri += 1
                        validVehiles.remove((vX,vY))
                        vki.append(vehicle_kiri)
                        
            # saatnya ngitung kendaraan =========================================kanan
            #for (vX, vY) in validVehiles:
                if vY > 450 and vY < 456: # adjust this for the frame jumping
                    if vX >670 and vX <1000:
                        vehicle_kanan += 1
                        validVehiles.remove((vX,vY))
                        vka.append(vehicle_kanan)
            
            #hr.append(now)
            
           
            
 
    # show the thresh and original video
    cv2.imshow('Foreground Mask', fgMask) # name of frame, caling the frame (masked)
    
    cv2.putText(frame, 'Date: {}'.format(now), (350,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)
    cv2.putText(frame, 'Total Vehicles : {}'.format(vehile), (520, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2) #put text
    
    cv2.putText(frame, 'Salatiga in : {}'.format(vehicle_kiri), (50, 90), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2) #put text
    cv2.putText(frame, 'Salatiga out: {}'.format(vehicle_kanan), (950, 90), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2) #put text

    cv2.imshow('Original Video', frame) # name of frame, caling the frame (original)
    

    
    with open('cobaappend.csv', 'w', newline='') as csvfile:
        fieldnames=['Date','Salatiga In','Salatiga Out','Total Vehicles']
        thewriter=csv.DictWriter(csvfile, fieldnames=fieldnames)
        thewriter.writeheader()
       # thewriter.writerow({'Date':now,'Salatiga In':vehicle_kiri,'Salatiga Out':vehicle_kanan,'Total Vehicles':vehile})
        thewriter.writerow({'Salatiga In':vki,'Salatiga Out':vka,'Total Vehicles':vto})
           
    
    # wait for any key to be pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# release video capture
cv2.destroyAllWindows()
vidCap.release()