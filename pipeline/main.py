from temp_name import *
# from shape_finder import *
from img_proc import *
from easyocr_test import find_numb
import easyocr


RobotMain.pprint('xArm-Python-SDK Version:{}'.format(version.__version__))
arm = XArmAPI('192.168.1.222', baud_checkset=False)
robot_main = RobotMain(arm)
# base = [6.022314, -0.203028, 0.008842, 0.133888, -1.652684, 2.99643, 0.0]
X_BASE = 16
Y_BASE = 6
Z_BASE = 16

def go_center(current, target):
    x_center = False
    z_center = False
    #robot_main.right(((target[0] - current[0]) //100) * 4)

    # print(current)
    # print(target)
    # print("--------")
    # if current[0] > target[0] - 40:
    #     robot_main.right()
    # elif current[0] < target[0] + 40:
    #     robot_main.left()

    # if current[1] < target[1] - 40:
    #     robot_main.down()
    # elif current[1] > target[1] + 40:
    #     robot_main.up()

    x,y,z = 0,0,0

    if current[0] < target[0] - 40:
        x = -X_BASE 
    elif current[0] > target[0] + 40:
        x = X_BASE
    else:
        x_center = True

    if current[1] < target[1] - 40:
        z = -Z_BASE
    elif current[1] > target[1] + 40:
        z = Z_BASE
    else:
        z_center = True

    robot_main.move(x,y,z)
    print("-----------------")
    print("current: ", current[0])
    print("target: ", target[0])
    print(x_center)
    print(z_center)
    print("-----------------")

    return x_center and z_center
    


if __name__ == '__main__':
    center = (320, 240)

    vis = vision(6)
    # vis2 = vision(4)

    # cooldown for OCR to make positioning for recognition easier
    frame_timer = 20

    while True:
        ret, frame = vis.cap.read()
        # ret2, frame2 = vis2.cap.read()

        if not ret:
            print("Failed to capture frame")
            break
        
        # if buttons are found and the target has not yet been identified
        if vis.shapes and not vis.target and frame_timer == 0:
            temp = find_numb(frame, '6')
            if temp:
                vis.target = ([[(temp[0][0]-temp[2][0])/2 + temp[2][0], ([temp[0][1]] - temp[2][1])/2 + temp[2][1]]], 1)
                # print(vis.target)
            print("Result ========= ", vis.target)

        vis.process_frame(frame)

        if vis.target and frame_timer == 0:
            # print(vis.target[-1])
            if go_center(center, vis.target[0][-1]):
            # if vis.target[-1] < 105:
            #     robot_main.forward()
                robot_main.forward()

        
        cv2.imshow('button Tracking', frame)
        # print(frame)
        # cv2.imshow('distance', frame2)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            robot_main.rest()
            break

        
        if frame_timer == 0:
            frame_timer = 20
        else:
            frame_timer -= 1

#320 x 240 image size
# x 6 pixels
# y 6-8 pixels