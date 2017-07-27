import cv2
import numpy as np

img = cv2.imread('test.png', 0)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=1, param2=1, minRadius=6, maxRadius=8)

circles = np.uint16(np.around(circles))
for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 1)
    # draw the center of the circle
    cv2.circle(cimg, (i[0], i[1]), 1, (0, 0, 255), 1)

cv2.imshow('detected circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
