import numpy as np
import cv2
import time

show = False

global triangle
global rectangle
global circle


def findBiggestShape():
    # Capturing video through webcam

    webcam = cv2.VideoCapture(0)
    ret = webcam.set(3, 640)
    ret = webcam.set(4, 480)
    frame_rate = 10
    prev = 0

    # Start a while loop
    while(1):

        # Reading the video from the
        # webcam in image frames

        time_elapsed = time.time() - prev
        _, imageFrame = webcam.read()
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            # Convert the imageFrame in
            # BGR(RGB color space) to
            # HSV(hue-saturation-value)
            # color space
            hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

            # Set range for red color and
            # define mask
            # red_lower = np.array([136, 87, 111], np.uint8)
            # red_upper = np.array([180, 255, 255], np.uint8)
            # red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

            # lower mask (0-10)
            lower_red = np.array([0, 50, 50])
            upper_red = np.array([10, 255, 255])
            mask0 = cv2.inRange(hsvFrame, lower_red, upper_red)

            # upper mask (170-180)
            lower_red = np.array([170, 50, 50])
            upper_red = np.array([180, 255, 255])
            mask1 = cv2.inRange(hsvFrame, lower_red, upper_red)

            # join my masks
            red_mask = mask0+mask1
            imageCanny_red = cv2.Canny(red_mask, 200, 250)

            # Set range for green color and
            # define mask
            # green_low = np.array([50, 52, 72], np.uint8)
            # green_upper = np.array([70, 255, 255], np.uint8)
            # green_mask = cv2.inRange(hsvFrame, green_low, green_upper)

            green_low = np.array([40, 40, 40], np.uint8)
            green_upper = np.array([70, 255, 255], np.uint8)
            green_mask = cv2.inRange(hsvFrame, green_low, green_upper)
            imageCanny_green = cv2.Canny(green_mask,  50, 150)

            # Set range for blue color and
            # define mask
            blue_lower = np.array([90, 80, 2], np.uint8)
            blue_upper = np.array([125, 255, 255], np.uint8)
            blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
            imageCanny_blue = cv2.Canny(blue_mask, 50, 150)

            # Morphological Transform, Dilation
            # for each color and bitwise_and operator
            # between imageFrame and mask determines
            # to detect only that particular color
            kernal = np.ones((5, 5), "uint8")

            # For red color
            red_mask = cv2.dilate(red_mask, kernal)
            res_red = cv2.bitwise_and(imageFrame, imageFrame,
                                      mask=red_mask)

            # For yellow color
            green_mask = cv2.dilate(green_mask, kernal)
            res_yellow = cv2.bitwise_and(imageFrame, imageFrame,
                                         mask=green_mask)

            # For blue color
            blue_mask = cv2.dilate(blue_mask, kernal)
            res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                                       mask=blue_mask)

            # Creating contour to track red color
            contours, hierarchy = cv2.findContours(imageCanny_red,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)

            i = 0
            rectangle = 0
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    # x, y, w, h = cv2.boundingRect(contour)
                    # imageFrame = cv2.rectangle(imageFrame, (x, y),
                    #                            (x + w, y + h),
                    #                            (0, 0, 255), 2)

                    if i == 0:
                        i = 1
                        continue

                    # cv2.approxPloyDP() function to approximate the shape
                    approx = cv2.approxPolyDP(
                        contour, 0.045 * cv2.arcLength(contour, True), True)

                    hull = cv2.convexHull(approx)
                    # print(len(approx))

                    # using drawContours() function
                    cv2.drawContours(imageFrame, [contour], 0, (0, 0, 255), 5)

                    # finding center point of shape
                    M = cv2.moments(contour)
                    if M['m00'] != 0.0:
                        x = int(M['m10']/M['m00'])
                        y = int(M['m01']/M['m00'])

                        # putting shape name at center of each shape
                        if len(approx) == 3:
                            cv2.putText(imageFrame, 'Triangle', (x, y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                        elif len(approx) == 4:
                            cv2.putText(imageFrame, 'Quadrilateral', (x, y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                            rectangle = rectangle + 1

                        else:
                            cv2.putText(imageFrame, 'circle', (x, y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                        # cv2.putText(imageFrame, "Red Colour", (x, y),
                        #             cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        #             (0, 0, 255))

            # Creating contour to track green color
            contours, hierarchy = cv2.findContours(imageCanny_green,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)

            i = 0
            triangle = 0
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    # x, y, w, h = cv2.boundingRect(contour)
                    # imageFrame = cv2.rectangle(imageFrame, (x, y),
                    #                            (x + w, y + h),
                    #                            (0, 255, 255), 2)

                    if i == 0:
                        i = 1
                        continue

                    # cv2.approxPloyDP() function to approximate the shape
                    approx = cv2.approxPolyDP(
                        contour, 0.045 * cv2.arcLength(contour, True), True)

                    hull = cv2.convexHull(approx)

                    # using drawContours() function
                    cv2.drawContours(imageFrame, [contour], 0, (0, 0, 255), 5)

                    # finding center point of shape
                    M = cv2.moments(contour)
                    if M['m00'] != 0.0:
                        x = int(M['m10']/M['m00'])
                        y = int(M['m01']/M['m00'])

                    # putting shape name at center of each shape
                    if len(approx) == 3:
                        cv2.putText(imageFrame, 'Triangle', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                        triangle = triangle + 1

                    elif len(approx) == 4:
                        cv2.putText(imageFrame, 'Quadrilateral', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    else:
                        cv2.putText(imageFrame, 'circle', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    # cv2.putText(imageFrame, "Yellow Colour", (x, y),
                    #             cv2.FONT_HERSHEY_SIMPLEX,
                    #             1.0, (0, 255, 255))

            # Creating contour to track blue color
            contours, hierarchy = cv2.findContours(imageCanny_blue,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)

            i = 0
            circle = 0
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    # x, y, w, h = cv2.boundingRect(contour)
                    # imageFrame = cv2.rectangle(imageFrame, (x, y),
                    #                            (x + w, y + h),
                    #                            (255, 0, 0), 2)

                    if i == 0:
                        i = 1
                        continue

                    # cv2.approxPloyDP() function to approximate the shape
                    approx = cv2.approxPolyDP(
                        contour, 0.045 * cv2.arcLength(contour, True), True)

                    hull = cv2.convexHull(approx)

                    # using drawContours() function
                    cv2.drawContours(imageFrame, [contour], 0, (0, 0, 255), 5)

                    # finding center point of shape
                    M = cv2.moments(contour)
                    if M['m00'] != 0.0:
                        x = int(M['m10']/M['m00'])
                        y = int(M['m01']/M['m00'])

                    # putting shape name at center of each shape
                    if len(approx) == 3:
                        cv2.putText(imageFrame, 'Triangle', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    elif len(approx) == 4:
                        cv2.putText(imageFrame, 'Quadrilateral', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    else:
                        cv2.putText(imageFrame, 'circle', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                        circle = circle + 1

                    # cv2.putText(imageFrame, "Blue Colour", (x, y),
                    #             cv2.FONT_HERSHEY_SIMPLEX,
                    #             1.0, (255, 0, 0))

            # Program Termination
            cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
            cv2.moveWindow('frame', x=0, y=0)  # 原地
            cv2.imshow('mask', imageCanny_red)
            cv2.moveWindow('mask', x=imageFrame.shape[1], y=0)  # 右边
            # print(rectangle)
            # print(triangle)
            # print(circle)
            prime = None
            if rectangle > triangle and rectangle > circle:
                # print("rectangle")
                prime = "rectangle"

            if triangle > rectangle and triangle > circle:
                # print("triangle")
                prime = "triangle"

            if circle > triangle and circle > rectangle:
                # print("circle")
                prime = "circle"

            if circle > triangle and circle == rectangle:
                # print("circle and rectangle")
                prime = "circle and rectangle"

            if circle > rectangle and circle == triangle:
                # print("circle and triangle")
                prime = "circle and triangle"

            if triangle > circle and triangle == rectangle:
                # print("triangle and rectangle")
                prime = "triangle and rectangle"

            if triangle > rectangle and triangle == circle:
                # print("triangle and circle")
                prime = "triangle and circle"

            if rectangle > circle and rectangle == triangle:
                # print("rectangle and triangle")
                prime = "rectangle and triangle"

            if rectangle > triangle and rectangle == circle:
                # print("rectangle and circle")
                prime = "rectangle and circle"

            if rectangle == triangle and rectangle == circle:
                # print("circle and rectangle and triangle")
                prime = "circle and rectangle and triangle"
            # cv2.imshow('res', res_red)
            # cv2.moveWindow('res', y=imageFrame.shape[0], x=0)  # 下边

            if cv2.waitKey(10) & 0xFF == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                return prime
                break


if __name__ == "__main__":
    findBiggestShape()
    print(findBiggestShape())
