import cv2
import serial
from cvzone.HandTrackingModule import HandDetector

# Initialize video capture and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.5, maxHands=1)
bt = serial.Serial('/dev/rfcomm4', 9600)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)

    # Detect hands in the frame
    hands, frame = detector.findHands(frame)

    if not hands:
        print("nothing")
    else:
        hands1 = hands[0]
        fingers = detector.fingersUp(hands1)

        # Count the number of fingers up
        count = fingers.count(1)
        print(count)

        # Send the count via Bluetooth
        string = 'X{0}'.format(count)
        bt.write(string.encode("utf-8"))

    # Display the frame
    cv2.imshow("FRAME", frame)

    # Break the loop if 'ESC' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
