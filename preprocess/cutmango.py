import cv2
total = 0
flag = 1
minus = 0
arr = []
maxi = 0
maxperc = 0
imgname =""
#input file format
#../Croppedmango/C2_TrainDev/Train/00001.jpg: Predicted in 14.289000 milli-seconds.
#mango: 99%      (left_x:  227   top_y:  276   width:  419   height:  398)

with open("parse_result4000dev") as f_name:
    for line in f_name:
        if 'jpg' in line:
            if len(arr) != 0:
                maxperc = 0
                maxi = 0
                for i in range(len(arr)):
                    if int(arr[i][1][:-1]) > maxperc:
                        maxperc = int(arr[i][1][:-1])
                        maxi = i
                x = int(arr[maxi][3])
                y = int(arr[maxi][5])
                w = int(arr[maxi][7]) 
                h = int(arr[maxi][9][:-1])
                #check x/width boundary
                if x < 0 and x+w < image.shape[1]:
                    w = w + x
                    x = 0
                if x < 0 and x+w >= image.shape[1]:
                    x = 0
                    w = image.shape[1]
                if x > 0 and x+w > image.shape[1]:
                    w = image.shape[1] - x
                #check y/height boundary
                if y < 0 and y+h < image.shape[0]:
                    h = h + y
                    y = 0
                if y < 0 and y+h >= image.shape[0]:
                    y = 0
                    h = image.shape[0]
                if y > 0 and y+h > image.shape[0]:
                    h = image.shape[0] - y

                cv2.imwrite("cut4000yolo_dev/"+imgname+".jpg",image[y : y+h, x : x+w]) 
                arr = []
            start = line.find("/Dev/") + 5
            end = line.find(".jpg")
            imgname = line[start:end]
            image = cv2.imread("Dev/" + imgname + ".jpg")
        if 'mango:' in line:
            arr.append(line.split())
    if len(arr) != 0:
        maxperc = 0
        maxi = 0
        for i in range(len(arr)):
            if int(arr[i][1][:-1]) > maxperc:
                maxperc = int(arr[i][1][:-1])
                maxi = i
        x = int(arr[maxi][3])
        y = int(arr[maxi][5])
        w = int(arr[maxi][7]) 
        h = int(arr[maxi][9][:-1])
        #check x/width boundary
        if x < 0 and x+w < image.shape[1]:
            w = w + x
            x = 0
        if x < 0 and x+w >= image.shape[1]:
            x = 0
            w = image.shape[1]
        if x > 0 and x+w > image.shape[1]:
            w = image.shape[1] - x
        #check y/height boundary
        if y < 0 and y+h < image.shape[0]:
            h = h + y
            y = 0
        if y < 0 and y+h >= image.shape[0]:
            y = 0
            h = image.shape[0]
        if y > 0 and y+h > image.shape[0]:
            h = image.shape[0] - y
        cv2.imwrite("cut4000yolo_dev/"+imgname+".jpg",image[y : y+h, x : x+w]) 
