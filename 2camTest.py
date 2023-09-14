import cv2

# Create VideoCapture objects for each webcam
cap1 = cv2.VideoCapture(1)  # USB webcam 1
cap2 = cv2.VideoCapture(2)  # USB webcam 2

# Check if the webcams opened successfully
if not cap1.isOpened() or not cap2.isOpened():
    print("Error: One or both webcams could not be opened.")
    exit()

while True:
    # Read frames from each webcam
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print("Error: Failed to read frames from one or both webcams.")
        break

    # Display the frames in separate windows
    cv2.imshow("Webcam 1", frame1)
    cv2.imshow("Webcam 2", frame2)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture objects and close all OpenCV windows
cap1.release()
cap2.release()
cv2.destroyAllWindows()
