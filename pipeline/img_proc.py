import cv2
import numpy as np
from rapid_ocr import find_numb

# Function to draw a line between two points
def draw_line(img, point1, point2, color=(0, 255, 0), thickness=2):
    cv2.line(img, tuple(map(int, point1)), tuple(map(int, point2)), color, thickness)

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    point1 = [float(point1[0]), float(point1[1])]
    point2 = [float(point2[0]), float(point2[1])]
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

class vision:

    def __init__(self, channel):

        self.MAX_HISTORY_LENGTH = 8
        self.MIN_HISTORY_LENGTH = 10
        self.shape_buffer = []

        self.cap = cv2.VideoCapture(channel)

        self.shapes = []

        self.target = []

        # To write a video 
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('move_test.mp4', fourcc, 20.0, (640*2, 480))
        self.out_alt = cv2.VideoWriter('vision.mp4', fourcc, 20.0, (640, 480))

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()


    def draw_frame(self, frame):
        # print(self.shapes)
        for shape in self.shapes:
                # print("test")
                cv2.circle(frame, center=shape[0], radius=shape[1], color=(0, 0, 255), thickness=-1)
        
        if self.target:
            cv2.circle(frame, center=self.target[0][-1], radius=self.target[1], color=(0, 255, 0), thickness=-1)
    

    def find_circles(self, img):
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
            minRadius=10,       
            maxRadius=110 # 50 voor de initiele herkinning voorkomt overbodige herkenning, 80 laat je dichterbij komen
        )

        if circles is not None:
            circles = np.uint32(np.around(circles))
        # print(circles)
        return circles if not circles is None else np.array([])


    def update(self):
        tracking_dist = 40
        best_dist = tracking_dist
        best_idx = None

        for index, value in enumerate(self.shapes):
            # print(value)
            center, radius = (value[0][0], value[0][1]), value[1]
            if self.target:
                dist = calculate_distance(center, self.target[0][-1]) 
                if dist < tracking_dist and dist < best_dist:
                    best_idx = index
                    best_dist = dist

        if best_idx is not None:
            center, radius = self.shapes.pop(best_idx)
            self.target[0].append(center)
            self.target = (self.target[0], radius)

        else:
            self.target = []
        
        if self.target:
            # print(self.target)
            history, radius = self.target
            self.target = (history[-self.MAX_HISTORY_LENGTH:], radius)
            # print(self.target[0])
        


    def process_frame(self, frame):
        
        found = self.find_circles(frame)
        
        if len(found) > 0:
            for i in found[0]:
                self.shapes.append(([i[0], i[1]], i[2]))

        # make video of camera and ui of shape detection
        blank_image = np.zeros((480,640*2,3), np.uint8)
        blank_image[:,0:640] = frame 
        self.update()
        self.draw_frame(frame)
        blank_image[:,640:640*2] = frame
        self.out.write(blank_image)


        self.shapes = self.shapes[-self.MAX_HISTORY_LENGTH:]


if __name__ == '__main__':
    vis = vision(6)
    # while True:
    #     ret, frame = vis.cap.read()
    #     if not ret:
    #         print("Failed to capture frame")
    #         break


    #     vis.process_frame(frame)
        
    #     cv2.imshow('Object Tracking', frame)
    #     # cv2.imshow('Object Tracking2', frame2)

    #     # Break the loop when 'q' is pressed
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #     # make photo when 'p' is pressed
    #     if cv2.waitKey(1) & 0xFF == ord('p'):
    #         cv2.imwrite("test.jpg", frame)
    while True:    
        ret, frame = vis.cap.read()
        frame_timer = 20

        if not ret:
            print("Failed to capture frame")
            break
        
        # if buttons are found and the target has not yet been identified
        if vis.shapes and not vis.target:
            temp = find_numb(frame, '6')
            if len(temp) > 0:
                vis.target = ([[(temp[0][0]-temp[2][0])/2 + temp[2][0], ([temp[0][1]] - temp[2][1])/2 + temp[2][1]]], 1)
                # print(vis.target)
            print("Result ========= ", vis.target)

        vis.process_frame(frame)
        
        cv2.imshow('button Tracking', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        
        if frame_timer == 0:
            frame_timer = 20
        else:
            frame_timer -= 1
        