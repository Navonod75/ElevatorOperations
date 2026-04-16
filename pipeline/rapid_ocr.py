from rapidocr import RapidOCR
import os

engine = RapidOCR()



def proc_img(photo):
        output = []
        result = engine(photo)
        if len(result) > 0:
                for index, value in enumerate(result.txts):
                        output.append((result.boxes[index], value,0))
        return output

def find_numb(photo, target):
        output = []
        result = engine(photo)
        if len(result) > 0:
                for index, value in enumerate(result.txts):
                        output.append((result.boxes[index], value,0))
        print(output)
        for i in output:
                if i[1] == target:
                        print(i[1])
                        return i[0]
        print("sad")
        return []

# result = engine("shapes_good.png")       
# result.vis("vis_result.jpg")

