import easyocr
import cv2
import os


reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory

def proc_img(path):
    # img_name = 'thesis/references/20251110_130508.jpg'



    return reader.readtext(path, paragraph=False)

          

