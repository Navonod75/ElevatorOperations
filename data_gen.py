from trdg.generators import (
    GeneratorFromDict,
    GeneratorFromRandom,
    GeneratorFromStrings,
    GeneratorFromWikipedia,
)
from PIL import Image

# The generators use the same arguments as the CLI, only as parameters
generator = GeneratorFromStrings(
    ['0','1', '2', '3','4','5','6','7','8','9'],
    blur=4,
    random_blur=True,
    size=32*9,
    count=1*10**6,
    skewing_angle=13,
    random_skew=True
)
curr = 0

for img, lbl in generator:
    if curr < 1*10**6 / 3:
        path = "/home/mike/School/thesis/training_data/"
    elif 1*10**6 / 3 < curr < 1*10**6 / 3 * 2:
        path = "/home/mike/School/thesis/eval/"
    else:
        path = "/home/mike/School/thesis/validation/"
    # path = "thesis/dataset/test/test.jpg"
    with open(path + "gt.txt", 'a+') as file:
        temp = path+lbl+"/number"+str(curr)+".jpg"
        img.save(temp)
        curr +=1
        output = f"{temp}\t{lbl}\n"
        file.write(output)
        print(path)