import cv2 as cv
cam = cv.VideoCapture(0)
while True:
    ret, frame = cam.read()
    if ret:
        cv.imshow("Feed",frame)
    key = cv.waitKey(5)
    if key ==27:
        break
cam.release()
cv.destroyAllWindows()