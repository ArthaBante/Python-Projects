# allows to interact with videos and images
import cv2

# allows to perform basic processing of images
import imutils

# allows to interact with sound
import winsound

# allows to execute other codes while waiting
import threading



# setting up the cameras, 0 for 1 camera, can choose more cameras
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Used to get the height and width of the frames in the video stream, measuring unit is in pixels
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# A "_" symbol indicates that it is private, and it cannot be used publicly
#Basic Idea: Get a starting frame and compare the difference with the next frame and if the difference is high enough then do something

# Gets a return value from camera, which will not be used, hence given _, and the frame returned by the camera
_, startframe = cap.read()

# sizing and coloring of the start frame
# smoothens the image
startframe = imutils.resize(startframe, width=500)
startframe = cv2.cvtColor(startframe, cv2.COLOR_BGR2GRAY)
startframe = cv2.GaussianBlur(startframe, (21, 21), 0)


# variable indicating is an alarm active right now, set to False
alarm = False

# Do we want to look for an alarm? In the beginning False by default
alarm_mode = False

# How long do we want the movement to happen to cause the alarm
alarm_counter = 0

# in here we will be defining what happens next when the alarm goes off
def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode: # Only cause the func when we are in alarm mode, but also want to terminate once we are out of the alarm mode
            break

        print("ALARM")
        winsound.Beep(2500, 1000)
    alarm = False

while True: # in here we are creating 1 more frame called frame, to find the difference btn the startframe and this one, or say to detect a movement


    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # this frame_bw is given the values of the end frame
        frame_bw = cv2.GaussianBlur(frame_bw, (5,5), 0)

        # checking the difference btn the first and the last frame
        difference = cv2.absdiff(frame_bw, startframe)


        #gray scales pixels, detects the motion with white color, it will either have 255 or 0.
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]

        # giving the value of the last frame to the first frame for the next iteration, so that the motion can be detected
        startframe = frame_bw

        # Defining the sensitivity of the movement detection, the lower the no the higher the sensitivity


        # Increase the alarm every time by 1,when the threshold is above
        if threshold.sum() > 300:
            alarm_counter +=1

        else:

            # Decrease the alarm every time by 1,when we dont see any movement
           if alarm_counter > 0:
               alarm_counter -= 1

        # showing the image when the alarm goes off and movement is detected
        cv2.imshow("Cam", threshold)

    else:
        #showing the image when the movement is not detected
        cv2.imshow("Cam", frame)

    # To make the beep sound
    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target = beep_alarm).start()

    # Defining that after pressing "t" the alarm will turn on
    key_press = cv2.waitKey(30)
    if key_press == ord("t"):
        alarm_mode = not  alarm_mode
        alarm_counter = 0


    # Defining that after pressing "q" the whole thing will shut off
    if key_press == ord("q"):
        alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()







