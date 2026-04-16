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

def find_numb(photo):
        output = []
        result = engine(photo)
        if len(result) > 0:
                for index, value in enumerate(result.txts):
                        output.append((result.boxes[index], value,0))
        return output

result = engine("shapes_good.png")       
result.vis("vis_result.jpg")