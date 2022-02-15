import multiprocessing
# import packages
#import headshots
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

from time import sleep
from gpiozero import LED, Buzzer, Servo
ledB = LED(17)
ledR = LED(18)
fan = LED(15)
alarm = Buzzer(12)

servo = Servo(19)
servo.value = -1      # set position to -1 => door is locked




#from picamera import PiCamera
#camera = PiCamera()
#from time import sleep # To preview on display time

#from gpiozero import AngularServo
#servo = AngularServo(19, initial_angle=90, min_pulse_width=0.0006, max_pulse_width=0.0023)

#Initialize 'currentname' to trigger only when a new person is identified.
#currentname1 = "Family"
currentname1 = "Unknown"

#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# load the known faces and embeddings along with
#OpenCV's Haar cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

# initialize the video stream and allow the camera sensor to warm up
#vs = VideoStream(src=2,framerate=10).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

# loop over frames from the video file stream
while True:
    def bar():
    
        
    #for i in range(100):
      #  print ("Tick")
        #time.sleep(1)

#if __name__ == '__main__':
    # Start bar as a process
        p = multiprocessing.Process(target=bar)
        p.start()

        # Wait for 10 seconds or until process finishes
        p.join(10)

        # If thread is still active

        time =0
        time.start()
        if time == 10:
            stop()
        #camera.capture('img.jpg')
        #camera.stop_preview()
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        # Detect the fce boxes
        boxes = face_recognition.face_locations(frame)
        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []


        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known encodings
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding)
            #name1 = "Family" 
            name1 = "Unknown" #if face is not recognized, then print Unknown
            
            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                
                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                
                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name1 = max(counts, key=counts.get)
                #name2 = max(counts, key=counts.get)
                
                #If someone in your dataset is identified
                # print their name on the screen
                # turn on an LED
                
                if (currentname1 != name1):
                    #currentname1 = name1
                    #print(currentname1)
                    print(name)
                    
                    
                #if (currentname1 != name2):
                    #currentname2 = name2
                   # print(currentname2)
                    ledB.on()  # blue led
                    fan.on()
                    alarm.on()               
                    sleep(5)            
                    alarm.off()
                    ledB.off()
                    fan.off()
                    
                    #servo.min()
                    #sleep(10)
                    #servo.mid()
                    # sleep(1)
                    #servo.on()
                    servo.max()
                    sleep(5)
                    servo.min()
                    #sleep(10)
                    #servo.off()
                    
                    #servo = AngularServo(19, initial_angle=0, min_pulse_width=0.0006, max_pulse_width=0.0023)
                    #servo.angle = 90
                    #sleep(5)
                    #servo.angle = 0
                    #sleep(5)
                    #servo.angle = -90
                    #sleep(5)
                              
                    #Turn the servo
                    #servo.angle = -45
                    #time.sleep = 5
                    #servo.angle = 45
                
               
               #servo.off()
                elif currentname1 == 'Unknown':
            
            
            
                    #currentname1 = name1
                    print(name1)
                    alarm.on()
                    ledR.on()
                    alarm.on()
                    # if currentname2 = name2:
                   
                else:
                    ledR.on()
                    #servo = AngularServo(20, initial_angle=0, min_pulse_width=0.0006, max_pulse_width=0.0023)
                    #servo.angle = 90
                    #sleep(5)
                    #servo.angle = 0
                    #sleep(5)
                    #servo.angle = -90
                    #sleep(5)
                        
                       #led.on()
                       #alarm.on()
                       # sleep(1)
                       # alarm.off()
                       # led.off()
                
                        
            # update the list of names
            names.append(name1)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image - color is in BGR
        cv2.rectangle(frame, (left, top), (right, bottom),
                      (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    .8, (0, 255, 255), 2)

    # display the image to our screen
    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(2) & 0xFF

    # quit when 'q' key is pressed
    if key == ord("q"):
        break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
 
