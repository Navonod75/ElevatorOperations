from easy_ocr_model import *
import time
import numpy as np
from shape_masking import find_circles

def load_data(annotation_file):
    annotations = dict()
    with open(annotation_file) as file:
        head = next(file)
        for line in file:
            photo,_,_,label,xmin,ymin,xmax,ymax = line.split(",")
            if photo in annotations:
                annotations[photo].append((label,xmin,ymin,xmax,ymax))
            else:
                annotations[photo] = [(label,xmin,ymin,xmax,ymax)]
    return annotations



def check_overlap(xmin_t, xmax_t, xmin_f, xmax_f, ymin_t,ymax_t,ymin_f,ymax_f):
    # print(xmin_t, xmax_t, xmin_f, xmax_f, ymin_t,ymax_t,ymin_f,ymax_f)
    x_dis = xmax_t - xmin_t
    y_dis = ymax_t - ymin_t

    horizontal_overlap = False
    vertical_overlap = False

    if ((xmin_t - xmin_f) < x_dis) or ((xmax_t - xmax_f) < x_dis):
        horizontal_overlap = True

    if ((ymin_t - ymin_f) < y_dis) or ((ymax_t - ymax_f) < y_dis):
        vertical_overlap = True
    
    return horizontal_overlap and vertical_overlap


def validate_model(path, annotations):
    total_found = 0
    total_correct = 0

    time_taken = []

    for photo in annotations:

        mask = find_circles(path + photo) # put mask on photo according to shape detection

        begin = time.perf_counter()

        # res = proc_img(path + photo)
        res = proc_img(mask)

        end = time.perf_counter()

        time_taken.append(end-begin)
        # print(max_time_taken)

        if len(res) > 0:
            # print(res)
            total_found += len(res)
            found = dict()
            for i in res:
                if i[-2] in found:
                    found[i[-2]].append(i)
                else:
                    found[i[-2]] = [i]

            for i in annotations[photo]:
                if i[0] in found:
                    for gevonden in found[i[0]]:
                        xmin,xmax,ymin,ymax = float(gevonden[0][0][0]), float(gevonden[0][1][0]), float(gevonden[0][0][1]), float(gevonden[0][2][1])
                        if check_overlap(float(i[1]),float(i[3]), xmin, xmax, float(i[2]), float(i[3]), ymin, ymax):
                            total_correct += 1
                            print(total_correct)
    
    return total_correct, total_found, time_taken

if __name__ == "__main__":
    annotations = load_data("button_dataset/valid/_valid_clean_annotations.csv")
    total_correct1, total_found1, time_taken1 = validate_model("button_dataset/valid/", annotations)

    annotations2 = load_data("button_dataset/train/_train_clean_annotations.csv")
    total_correct2, total_found2, time_taken2 = validate_model("button_dataset/train/", annotations2)

    annotations3 = load_data("button_dataset/test/_test_clean_annotations.csv")
    total_correct3, total_found3, time_taken3 = validate_model("button_dataset/test/", annotations3)
    

    print("amount of images = ",len(annotations)+ len(annotations2)+ len(annotations3))
    print("total correct = ", total_correct1+ total_correct2 + total_correct3)
    print("total found = ",total_found1+ total_correct2 + total_found3)
    print("max time taken = ", max([max(time_taken1), max(time_taken3), max(time_taken2)]))
    time_taken1.extend(time_taken2)
    time_taken1.extend(time_taken3)
    print("avg time = ", str(np.mean(time_taken1)))



# easy ocr:
# amount of images =  1615
# total correct =  846
# total found =  1334
# max time taken =  1.2239815210000415
# avg time =  0.5212468246334346

# masked easy:
# amount of images =  1615
# total correct =  108
# total found =  130
# max time taken =  1.2219608849991346
# avg time =  0.45717685958697646







# rapid ocr:
# amount of images =  1615
# total correct =  1784
# total found =  2491
# max time taken =  0.9155855800008794
# avg time =  0.3472041980074311

#masking rapid:
# amount of images =  1615
# total correct =  354
# total found =  405
# max time taken =  0.7266073850005341
# avg time =  0.15735902793683457