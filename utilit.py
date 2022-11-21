import cv2
import numpy as np
import random

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cam.set(cv2.CAP_PROP_EXPOSURE, -6)

arr_x = {"b": 0, "y": 0, "g": 0}
check = ['g','y','b']
random.shuffle(check)
print(check)
def contours(m):
    return cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def circle(c):
     if len(c) > 0:
        c = max(c, key=cv2.contourArea)
        (x,y), radius = cv2.minEnclosingCircle(c)
        cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 255), 2)
        colour_arr = hsv[int(y),int(x)]
        #print(colour_arr)
        if lower_blue[0] <= colour_arr[0] <= upper_blue[0] \
         and lower_blue[1] <= colour_arr[1] <= upper_blue[1] \
         and lower_blue[1] <= colour_arr[1] <= upper_blue[1]: 
        #  print("blue")
        #  print(x, y)
         arr_x["b"] = x
        if lower_yellow[0] <= colour_arr[0] <= upper_yellow[0] \
         and lower_yellow[1] <= colour_arr[1] <= upper_yellow[1] \
         and lower_yellow[1] <= colour_arr[1] <= upper_yellow[1]: 
        #  print("yellow")
        #  print(x, y)
         arr_x["y"] = x
        if lower_green[0] <= colour_arr[0] <= upper_green[0] \
         and lower_green[1] <= colour_arr[1] <= upper_green[1] \
         and lower_green[1] <= colour_arr[1] <= upper_green[1]: 
        #  print("green")
        #  print(x, y)
         arr_x["g"] = x
         if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
     if arr_x["g"] and arr_x["y"] and arr_x["b"] != 0:
        sorted_dict = dict(sorted(arr_x.items(), key=lambda x: x[1]))
        #print(list(sorted_dict.keys()))
        if list(sorted_dict.keys())[0] == check[0] and list(sorted_dict.keys())[1] == check[1] and list(sorted_dict.keys())[2] == check[2]:
            print("Nice!")
            

        

def result(m):
    return cv2.bitwise_and(frame, frame, mask = m)

measures = []
hsv = []
while cam.isOpened():
    ret, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([80,200,40])
    upper_blue = np.array([110,250,93])

    lower_green = np.array([50,200,40])
    upper_green = np.array([80,250,93])

    lower_yellow = np.array([10,190 ,90])
    upper_yellow = np.array([50,250,150])

    lower_red = np.array([150,150,40])
    upper_red = np.array([190,200,93])

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    contours_blue, _ = contours(mask_blue)
    contours_yellow, _ = contours(mask_yellow)
    contours_green, _ = contours(mask_green)

    res_b = result(mask_blue)
    res_y = result(mask_yellow)
    res_g = result(mask_green)

    circle(contours_blue)
    circle(contours_yellow)
    circle(contours_green)

    cv2.imshow("Camera", frame)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()