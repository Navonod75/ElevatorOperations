import cv2
import numpy as np


def find_circles(img_name):
        img = cv2.imread(img_name)
        output = img.copy()
        # grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Reduce noise
        gray = cv2.medianBlur(gray, 5)

        # Detect circles
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=50,      
            param1=100,         
            param2=50,       
            minRadius=2,       
            maxRadius=150 # iterative adjjustment? vereist wel kennis over wat er te verwachten valt
        )

        mask = np.zeros(img.shape[:2], dtype=np.uint8)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0]:
                x, y, r = circle
                cv2.circle(mask, (x, y), r, 255, -1)  # Circle outline

        print(circles)
        masked_img = cv2.bitwise_and(output, output, mask=mask)

        # cv2.imshow('masked', masked_img)
        # cv2.imshow('og', output)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        print("button_dataset/masked/"+ img_name.split('/')[-1])
        cv2.imwrite("button_dataset/masked/"+ img_name.split('/')[-1], masked_img)

        return "button_dataset/masked/"+ img_name.split('/')[-1]