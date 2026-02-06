import cv2
import numpy as np

# Function to draw a line between two points
def draw_line(img, point1, point2, color=(0, 255, 0), thickness=2):
    cv2.line(img, tuple(map(int, point1)), tuple(map(int, point2)), color, thickness)

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


class vision:

    def __init__(self, channel):

        self.MAX_HISTORY_LENGTH = 30
        self.MIN_HISTORY_LENGTH = 10
        self.shape_buffer = []

        self.cap = cv2.VideoCapture(channel)

        self.shapes = []

        self.target = []
        

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()


    def find_circles(self, img):
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
            minRadius=10,       
            maxRadius=70 # 50 voor de initiele herkinning voorkomt overbodige herkenning, 80 laat je dichterbij komen
        )
        #! print(circles)
        # Draw only the first detected circle
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0]:
                x, y, r = i
                cv2.circle(output, (x, y), r, (0, 0, 255), 2)  # Circle outline
                cv2.circle(output, (x, y), 2, (0, 0, 255), 3)  # Center point

        return circles



    def draw_frame(self, frame):
        for shape in self.shapes:
            if shape[-1] == "circ":
                if not self.target:
                    cv2.circle(frame, center=shape[0][-1], radius=shape[1], color=(0, 0, 255), thickness=-1)
                else:
                    cv2.circle(frame, center=shape[0][-1], radius=shape[1], color=(0, 255, 0), thickness=-1)

    

    def update_shapes(self, found, frame):

        if self.target:
            for i in self.shapes:
                # print("i: ", i)
                # print("target: ", self.target)
                if (self.target[0][0] <= i[0][0][0] <= self.target[2][0]) and (self.target[0][1] <= i[0][0][1] <= self.target[2][1]):
                    self.shapes = [i]

        new_shapes = []
        for circ in found:
            center, radius = (circ[0], circ[1]), circ[2]

            # Check if circle is already in the list
            found_similar = False
            for existing_circ in self.shapes:
                if existing_circ[-1] != "circ":
                    continue
                if calculate_distance(center, existing_circ[0][-1]) < 20:  # Adjust the threshold as needed
                    print("test")
                    for i in range(1, len(existing_circ[0])):
                        draw_line(frame, existing_circ[0][i - 1], existing_circ[0][i])
                    existing_circ[0].append(center)
                    new_shapes.append(existing_circ)
                    found_similar = True
                    break
            # If no similar circle is found, add the current circle to the list
            if not self.target:
                if not found_similar:
                    history = [center]
                    self.shape_buffer.append((history, radius, "circ"))


                for existing_circ in self.shape_buffer:
                    if existing_circ[-1] != "circ":
                        continue
                    if calculate_distance(center, existing_circ[0][-1]) < 20:  # Adjust the threshold as needed
                        existing_circ[0].append(center)
                        break

        self.shapes = new_shapes

        for i in range(len(self.shape_buffer) - 1, -1, -1):
            # print(self.shape_buffer[i][0])
            if len(self.shape_buffer[i][0]) >= self.MIN_HISTORY_LENGTH:
                self.shapes.append(self.shape_buffer.pop(i))
        
            # Trim the history to the maximum length

        # print(shapes)
        for i, (history, _, _) in enumerate(self.shapes):
            self.shapes[i] = (history[-self.MAX_HISTORY_LENGTH:], radius, _)
        
        return self.shapes

    def process_frame(self, frame):
        #find circles
        circles = self.find_circles(frame)
        if circles is not None:
            self.shapes = self.update_shapes(circles[0], frame)
        else: 
            for i in range(len(self.shapes)-1, -1, -1):
                if self.shapes[i][-1] == "circ":
                    self.shape_buffer.append(self.shapes.pop(i))
        # if circles is not None:
        #     for circ in circles:
        #         cv2.circle(frame, center=circ[:2], radius=circ[2], color=(0, 0, 255), thickness=-1)  

        # find rectagles
        #! TODO

        # update found shapes
        

        self.draw_frame(frame)
        return self.shapes


if __name__ == '__main__':
    vis = vision(6)
    # vis2 = vision(4)

    while True:
        ret, frame = vis.cap.read()
        # ret2, frame2 = vis2.cap.read()

        if not ret:
            print("Failed to capture frame")
            break

        # if cv2.waitKey(1) & 0xFF == ord('p'):
        #     print("test")
        #     cv2.imwrite("/home/mike/School/thesis/pipeline/ocr_test/file.jpg", frame)

        vis.shapes = vis.process_frame(frame)
        
        cv2.imshow('Object Tracking', frame)
        # cv2.imshow('Object Tracking2', frame2)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Break the loop when 'p' is pressed
        