import cv2
total = 0
flag = 0
image = 0
i_file = 0
image_h = 0
image_w = 0
#input file format
#../Croppedmango/C2_TrainDev/Train/00001.jpg: Predicted in 14.289000 milli-seconds.
#mango: 99%      (left_x:  227   top_y:  276   width:  419   height:  398)

with open("parse_result10000") as f_name:
    for i, line in enumerate(f_name):
        if 'jpg' in line:
            if flag == 1:
                cv2.imwrite("tempt/"+i_file, image)
            flag = 1
            i_file = line[line.find(".jpg")-5 : line.find(".jpg")+4]
            image = cv2.imread("Train/" + i_file)
            (image_h, image_w) = image.shape[:2]
            continue
        if 'mango' in line:
            line = line.split()
            x = int(line[3])
            y = int(line[5])
            w = int(line[7])
            h = int(line[9][:-1])
            if flag == 1:
                if w > image_w and h > image_h:
                    cv2.rectangle(image, (0, 0), ( image_w, image_h), (255,77,210), 5)
                else:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255,77,210), 5)
    cv2.imwrite("tempt/" + i_file, image)
