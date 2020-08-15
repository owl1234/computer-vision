import numpy as np
import cv2 as cv
import math
cap = cv.VideoCapture(0)

#signs = ["road_works.png", "parking.png", "stop.png", "way_out.png"]
#signs = ["a_unevenness.png", "main_road.png", "no_drive.png", "no_entry.png", "parking.png", "stop.png", "way_out.png"]
signs = ["a_unevenness.png", "main_road.png", "no_drive.png", "no_entry.png", "parking.png", "pedistrain.png", "road_works.png", "stop.png", "way_out.png"]

arrays = []
last_name = ""
percent = [0] * len(signs)
# lower = np.array([127, 127, 127])
#lower = np.array([0, 10, 170])
lower = np.array([0, 34, 138])
upper = np.array([255, 255, 255])
for i in range(len(signs)):
   noDrive = cv.imread(signs[i])
   noDrive=cv.resize(noDrive,(40, 40))
   xnoDrive=cv.inRange(noDrive, lower, upper)
   arrays.append(xnoDrive)

while(True):
   ret, frame = cap.read()
   hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
   hsv = cv.blur(hsv, (5, 5))

   thresh = cv.inRange(hsv, lower, upper)

   thresh = cv.erode(thresh, None, iterations=2)
   thresh = cv.dilate(thresh, None, iterations=4)

   contours = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
   contours=contours[1]
   #last_name = ""
   count = 0
   for cnt in contours:
      c = sorted(contours, key=cv.contourArea, reverse=True)[0]
      rect = cv.minAreaRect(c)
      box = np.int0(cv.boxPoints(rect))
      cv.drawContours(frame, [box], -1, (0, 255, 0), 3)  # draw contours in green color
      cv.imshow("test",frame)
      y1 = int(box[0][1])
      x2 = int(box[1][0])
      y2 = int(box[1][1])
      x3 = int(box[2][0])

      roiImg = frame[y2:y1, x2:x3]

      if roiImg.any():
         cv.imshow('roiImg', roiImg)
         resizedRoi = cv.resize(roiImg, (40, 40))
         xresizedRoi = cv.inRange(resizedRoi, lower, upper)


         for i in range(len(signs)):

            identity_percent=0

            for ii in range(30):
               for j in range(40):
                  if (xresizedRoi[ii][j]==arrays[i][ii][j]):
                     identity_percent += 1

            if identity_percent < 800:
               continue

            percent[i] += identity_percent

         count += 1
         #if
         #if


         if count == 25:
            count = 1
            max_percent = max(percent)
            name = signs[percent.index(max_percent)].split('.')[0]
            percent = [0] * len(signs)
            if name != last_name:
               print(name)
               last_name = name


   cv.imshow('frame', frame)

   if cv.waitKey(1) & 0xFF == ord('q'):
       break
cap.release()
cv.destroyAllWindows()
