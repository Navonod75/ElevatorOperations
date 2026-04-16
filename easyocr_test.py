import easyocr
import cv2
import os

if __name__ == '__main__':
    # img_name = 'thesis/references/20251110_130508.jpg'
    alpha = 0.4


    reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory


    for file in os.scandir("../thesis"):
        if file.name == "shapes_good.png":
            print(file.name)
            if file.is_file():
                img_name = "../thesis/" + file.name
                result = reader.readtext(img_name, paragraph=False)

                # for item in result:
                #     print(item)

                img = cv2.imread(img_name)
                image_new = img.copy()
                print(result)
                for box in result:
                    overlay = image_new.copy()
                    cv2.rectangle(overlay,(int(box[0][0][0]), int(box[0][0][1])),(int(box[0][2][0]), int(box[0][2][1])),(0,255,0),-1)
                    image_new = cv2.addWeighted(overlay, alpha, image_new, 1 - alpha, 0)

                cv2.imwrite("../thesis/easy_res/" + file.name, image_new)


def find_numb(img, target):
    
    reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory

    result = reader.readtext(img, paragraph=False)
    print(result)
    
    for i in result:
        if i[0][2] == target:
            return i[0][0]
        
    return []
