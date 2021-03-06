import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

#signs = ["road_works.png", "parking.png", "stop.png", "way_out.png"]
signs = ["main_road.png", "no_drive.png", "no_entry.png", "parking.png", "stop.png", "way_out.png"]
# signs = ["a_unevenness.png", "main_road.png", "no_drive.png", "no_enrty.py", "parking.png", "pedistrain.png", "road_works.png", "stop.png", "way_out.png"]

arrays = []
last_name = ""
#lower = np.array([0, 90, 73])
#lower = np.array([0, 10, 170])
lower = np.array([0, 90, 138])
upper = np.array([255, 255, 255])
for i in range(len(signs)):
   noDrive = cv.imread(signs[i])
   noDrive=cv.resize(noDrive,(40, 40))
   xnoDrive=cv.inRange(noDrive, lower, upper)
   arrays.append(xnoDrive)

while(True):
   ret, frame = cap.read()
   #print (ret)
   hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

   hsv = cv.blur(hsv, (5, 5))


   thresh = cv.inRange(hsv, lower, upper)

   thresh = cv.erode(thresh, None, iterations=2)
   thresh = cv.dilate(thresh, None, iterations=4)

   contours = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
   contours=contours[1]
   #last_name = ""
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

         percent = [0] * len(signs)
         for i in range(len(signs)):

            identity_percent=0
            for ii in range(20):
               for j in range(20):
                  #print(arrays[i][ii][j])
                  if (xresizedRoi[ii][j]==arrays[i][ii][j]):
                     identity_percent=identity_percent+1

            for ii in range(20, 40):
               for j in range(20, 40):
                  if (xresizedRoi[ii][j]==arrays[i][ii][j]):
                     identity_percent=identity_percent+1
            percent[i] = identity_percent
            #print(signs[i], '-', percent[i])
            #if percent[i] > 8000:
            #   break
         max_percent = max(percent)
         name = signs[percent.index(max_percent)].split('.')[0]

         if name != last_name:
            print(name)
            last_name = name


   cv.imshow('frame', frame)

   if cv.waitKey(1) & 0xFF == ord('q'):
       break
cap.release()
cv.destroyAllWindows()
