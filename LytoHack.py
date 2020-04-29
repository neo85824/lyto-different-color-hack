import cv2
import numpy as np
import sys
from PIL import ImageGrab
import pyautogui
import time

autoGaming = False
autoGamingMs = 10
WaitMs = 10
window_size = 350

# find the screen resolution
screen = np.asarray(ImageGrab.grab(), dtype=np.uint8)
screen_h , screen_w = screen.shape[0], screen.shape[1]
# set up the cropping window size
box_w = 400
box_h = 400
start_x = screen_w//2 - box_w//2
start_y = screen_h//2 - box_h//2

while True:
    # screenshot for the certain area
    img = ImageGrab.grab(bbox=(start_x, start_y, start_x+box_w, start_y+box_h)) 
    img_bgr = np.array(img)
    
    circles = cv2.HoughCircles(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY) , cv2.HOUGH_GRADIENT,1,10,param1=40,param2=40,minRadius=0,maxRadius=100)
    if circles is None:
        print('No circles detected')
        continue
    
    # calculate the radius mean and std of all detected circle 
    r_mean = circles[0,:,2].mean()
    r_std = circles[0,:,2].std()
    tol = 2  # tolarence of std 
    Ans_idx = -1
    # get the bgr colors from the center of circle
    colors = img_bgr[circles[0, :, 1].astype(np.int), circles[0, :, 0].astype(np.int), :]
    # find out the color which appears the most of all circles
    values, counts = np.unique(colors, return_counts=True, axis=0)
    mode_color = values[np.argmax(counts)]
    
    for idx, c in enumerate(circles[0,:]):
        # compare the center color of circle and check the radius of the current circle is valid or not. (the threshold will be  mean - tol*std < r < mean + tol*std )
        if not np.array_equal(img_bgr[c[1].astype(np.int), c[0].astype(np.int)], mode_color) and r_mean- tol*r_std <= c[2] < r_mean+ tol*r_std:
            # draw circle and the center
            cv2.circle( img_bgr,(c[0], c[1]), c[2], (0,255,0), 2)
            cv2.circle( img_bgr,(c[0], c[1]), 2, (0,0,255), 3)
            Ans_idx = idx 

    cv2.imshow("LytoColorHack",	cv2.cvtColor(cv2.resize(img_bgr, (window_size, window_size)), cv2.COLOR_BGR2RGB))

    if autoGaming and Ans_idx >= 0:       
        ans_x, ans_y, ans_r = circles[0, Ans_idx]
        # Preserve current mouse position
        prevMouse = pyautogui.position()

        # Click the indentified circle on the main screen
        pyautogui.click(x=(start_x + ans_x), y=(start_y + ans_y))
        pyautogui.click(*prevMouse)

        time.sleep(autoGamingMs/1000) 

    elif Ans_idx == -1:
        print('Cannot find the answer')


    key = cv2.waitKey(WaitMs)
    if key == 27:
        break
    elif key == ord('s'):
        if autoGaming:
            print('Stop auto-gaming')
            autoGaming = False
        else:
            print('Start auto-gaming')
            autoGaming = True

cv2.destroyAllWindows()