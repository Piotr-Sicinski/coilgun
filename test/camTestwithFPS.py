import numpy as np
import cv2
import datetime
import sys
import argparse
import time


def test(enableGraphics: bool):
    exp = -6

    print(cv2.__version__)

    # create display window
    if enableGraphics:
        cv2.namedWindow("webcam", cv2.WINDOW_NORMAL)

    # initialize webcam capture object
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 5)

    # retrieve properties of the capture object
    cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap_fps = cap.get(cv2.CAP_PROP_FPS)
    cap_exp = cap.get(cv2.CAP_PROP_EXPOSURE)
    print('* Capture exposure:', cap_exp)
    print('* Capture width:', cap_width)
    print('* Capture height:', cap_height)
    print('* Capture FPS:', cap_fps)

    # cap.set(cv2.CAP_PROP_EXPOSURE, exp)

    # initialize time and frame count variables
    last_time = datetime.datetime.now()
    frames = 0

    # main loop: retrieves and displays a frame from the camera
    while (True):
        # blocks until the entire frame is read
        success, img = cap.read()
        # time.sleep(1/cap_fps)

        if not success:  # no image captured... end the processing
            sys.stderr.write("Could not read camera frame. Quitting\n")
            sys.exit(1)

        frames += 1

        # compute fps: current_time - last_time
        delta_time = datetime.datetime.now() - last_time
        elapsed_time = delta_time.total_seconds()
        cur_fps = np.around(frames / elapsed_time, 1)

        # draw FPS text and display image
        if enableGraphics:
            cv2.putText(img, 'FPS: ' + str(cur_fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("webcam", img)

        # wait 1ms for ESC to be pressed
        key = cv2.waitKey(1)
        if (key == 27):
            break

        if (chr(key & 255) == 'n'):
            exp -= 1
            cap.set(cv2.CAP_PROP_EXPOSURE, exp)

        if (chr(key & 255) == 'm'):
            exp += 1
            cap.set(cv2.CAP_PROP_EXPOSURE, exp)

        if frames % 50 == 0:
            # print(cap.get(cv2.CAP_PROP_EXPOSURE))
            print(cur_fps)

    # release resources
    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run FPS Test')
    parser.add_argument('-g', '--graphics',
                        action='store_false',
                        help='Disable-Graphics')
    params = parser.parse_args()

    test(params.graphics)
