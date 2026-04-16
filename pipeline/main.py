from temp_name import *
# from shape_finder import *
from img_proc import *
from rapid_ocr import find_numb
import easyocr
from rapidocr import RapidOCR
import time


RobotMain.pprint('xArm-Python-SDK Version:{}'.format(version.__version__))
arm = XArmAPI('192.168.1.222', baud_checkset=False)
robot_main = RobotMain(arm)
# base = [6.022314, -0.203028, 0.008842, 0.133888, -1.652684, 2.99643, 0.0]
X_BASE = 16
Y_BASE = 6
Z_BASE = 16

def go_center(current, target, radius):
    
    x_center = False
    z_center = False

    error_margin = 30
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

    if radius > 80:
        z = Z_BASE
        robot_main.move(x,y,z)
        robot_main.forward()
        robot_main.forward()
        robot_main.rest()
        
        return x_center and z_center
    


    if current[0] < target[0] - error_margin:
        x = -X_BASE 
    elif current[0] > target[0] + error_margin:
        x = X_BASE
    else:
        x_center = True

    if current[1] < target[1] - error_margin:
        z = -Z_BASE
        robot_main.forward(10, True)
    elif current[1] > target[1] + error_margin:
        z = Z_BASE
    else:
        z_center = True

    robot_main.move(x,y,z)
    
    # print("-----------------")
    # print("current: ", current[0])
    # print("target: ", target)
    # print(x_center)
    # print(z_center)
    # print("-----------------")

    return x_center and z_center
    


if __name__ == '__main__':
    target_num = "0"

    curr_time = str(time.localtime().tm_hour) + str(time.localtime().tm_min)

    positions = open("positions_"+target_num+"_"+curr_time+".txt", "w")
    center = (320, 240)

    vis = vision(6)

    # cooldown for OCR to make positioning for recognition easier
    frame_timer = 20

    while True:
        ret, frame = vis.cap.read()

        if not ret:
            print("Failed to capture frame")
            break
        # if buttons are found and the target has not yet been identified
        if vis.shapes and not vis.target and frame_timer == 0:
            temp = find_numb(frame, target_num)
            if len(temp) > 0:
                vis.target = ([[(temp[0][0]-temp[2][0])/2 + temp[2][0], ([temp[0][1]] - temp[2][1])/2 + temp[2][1]]], 1)
                # print(vis.target)

        positions.write(str(arm.get_position()[1]) + "\n")
        vis.process_frame(frame)

        if vis.target and frame_timer == 0:
            print(vis.target[-1])
            if go_center(center, vis.target[0][-1], vis.target[-1]):
            # if vis.target[-1] < 105:
            #     robot_main.forward()
                robot_main.forward()

        
        cv2.imshow('button Tracking', frame)


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