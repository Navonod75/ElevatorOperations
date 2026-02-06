from rapidocr import RapidOCR
import os

engine = RapidOCR()

for file in os.scandir("thesis/references"):
    if file.is_file():
        # print(file.name)

        img_url = "thesis/references/" + file.name
        result = engine(img_url)
# print(result)

        result.vis("thesis/result_img/" + file.name)


# img_url = "thesis/references/20251110_1305170.jpg"
# result = engine(img_url)
# result.vis("thesis/result_img/test.jpg")

# print(result.txts)

# engi