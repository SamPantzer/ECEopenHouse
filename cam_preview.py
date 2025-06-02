#!/usr/bin/env python3
import numpy as np
import time
time.sleep(1) # allow camera to intiallize before running script
import os
os.system("unclutter-xfixes -idle 1 &") # hide cursor when inactive
from picamera2 import Picamera2
import cv2

# Configs for camera
os.environ["DISPLAY"] = ":0"
picam2 = Picamera2()
# set size and white balance
config = picam2.create_preview_configuration({'size': (800,480),'format': 'RGB888'})
picam2.configure(config)
picam2.awb_mode = "on"
picam2.start()

#GLOBAL VARIABLES

recorded_frames = [] # recorded frames in memory (no FOIP concerns)
playback_index = 0

# button config
button_center = (800-60,60)
button_radius = 40
button_colour = (0,0,255)

# flash animation
flash_duration = 5
button_pressed = False
flash_start_time = 0
flash_interval = 0.3

#init camera window
cv2.namedWindow("Preview", cv2.WINDOW_GUI_EXPANDED)
cv2.setWindowProperty("Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def draw_button(frame, radius):
    cv2.circle(frame, button_center, radius, button_colour, -1)

# call back function every time the button is clicked, checks that
# mouse within button size
def record_callback(event, x, y, flags, param):
    global button_pressed, flash_start_time
    if event == cv2.EVENT_LBUTTONDOWN:
        dist = np.sqrt((x-button_center[0])**2 + (y-button_center[1])**2)
        if dist <= button_radius:
            button_pressed = True
            flash_start_time = time.time()

cv2.setMouseCallback("Preview", record_callback)

# main event loop
while True:
    frame = picam2.capture_array() # captures camera feed
    if button_pressed == True: # start recording
        if time.time() - flash_start_time < flash_duration: # record for 5 seconds
            recorded_frames.append(frame.copy()) # appends recorded frame in memory
            # begins falshing animation for button
            flashes = int((time.time()-flash_start_time) / flash_interval)
            if flashes % 2 == 0:
                draw_button(frame, 0) # hides button
            else:
                draw_button(frame, button_radius) # shows button
        else: # Start playback
            if playback_index < len(recorded_frames):
                frame = recorded_frames[playback_index]
                draw_button(frame, 0) # hides button during playback
                cv2.imshow("Preview", frame)
                time.sleep(1/60) # 60 fps
                playback_index += 1
            else:
                button_pressed = False # exit branch
    else: # continue preview
        draw_button(frame, button_radius) # show button
    cv2.imshow("Preview", frame)
    if cv2.waitKey(1) == ord("q"): # breakout key
        break
    
cv2.destroyAllWindows()
picam2.stop()
