'''
speed does not seem to get better then 5 seconds with logitech c920
'''
# import the necessary packages
import detect_barcode
import argparse
import subprocess
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the (optional) video file")
args = vars(ap.parse_args())

# if the video path was not supplied, grab the reference to the
# camera
if not args.get("video", False):
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    #camera = cv2.VideoCapture(0)

# otherwise, load the video
else:
    camera = cv2.VideoCapture(args["video"])

prev = ''
# keep looping over the frames
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    # check to see if we have reached the end of the
    # video
    if not grabbed:
        break

    # detect the barcode in the image
    box = detect_barcode.detect(frame)

    if box is not False:
        # if a barcode was found, draw a bounding box on the frame
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
        cv2.imshow("Frame", frame)
        #cv2.imwrite('barcode.jpg', frame)
        '''
        zbar = subprocess.Popen(['/usr/bin/zbarimg', '-q', '--nodisplay', 'barcode.jpg'], stdout=subprocess.PIPE)

        code = zbar.stdout.readline()  # thread stuck here waiting for barcode

        if code == '':  # need this if zbarcam is killed
            code = ':'

        barcode = code.split(':')[1].rstrip('\n')  # strip out everything before and including :

        # got a barcode reset timer
        if barcode is not '':
            if not barcode == prev:
                print barcode
                prev = barcode
        '''
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()