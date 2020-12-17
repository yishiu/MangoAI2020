import cv2
total = 0
minus = 0
arr = []
maxi = 0
maxperc = 0
imgname =""
#parse_result file format
#../Croppedmango/C2_TrainDev/Train/00001.jpg: Predicted in 14.289000 milli-seconds.
#mango: 99%      (left_x:  227   top_y:  276   width:  419   height:  398)
def formatnum(v):
        return "%.6f" % v

with open("parse_result8000") as f_name, open("train.csv") as f_dis:
    for line in f_name:
        if '.jpg' in line:
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
                #write to file
                disease_list = None
                for find_name in f_dis:
                    if imgname+".jpg" in find_name:
                        disease_list =  find_name.split(',')
                        break
                f_dis.seek(0)
                idx_row = 1
                f_txt = open("tempt/" + imgname + ".txt", "w")
                while True:
                    dis_x = int(float(disease_list[idx_row]))
                    dis_y = int(float(disease_list[idx_row+1]))
                    dis_w = int(float(disease_list[idx_row+2]))
                    dis_h = int(float(disease_list[idx_row+3]))
                    ###
                    if  "不良-乳汁吸附" in disease_list[idx_row+4]: #02176.jpg has this item in last column, so include \n
                        if x <= dis_x and x+w >= dis_x+dis_w and y <= dis_y and y+h >= dis_y+dis_h:
                            f_txt.writelines('0 '+ str(dis_x-x)+ ' ' + str(dis_y-y)+ ' '+ str(dis_w)+' ' + str(dis_h) + '\n')
                    elif disease_list[idx_row+4] == "不良-機械傷害":
                        if x <= dis_x and x+w >= dis_x+dis_w and y <= dis_y and y+h >= dis_y+dis_h:
                            f_txt.writelines('1 '+ str(dis_x-x)+ ' ' + str(dis_y-y)+ ' '+ str(dis_w)+' ' + str(dis_h) + '\n')
                    elif disease_list[idx_row+4] == "不良-炭疽病":
                        if x <= dis_x and x+w >= dis_x+dis_w and y <= dis_y and y+h >= dis_y+dis_h:
                            f_txt.writelines('2 '+ str(dis_x-x)+ ' ' + str(dis_y-y)+ ' '+ str(dis_w)+' ' + str(dis_h) + '\n')
                    elif disease_list[idx_row+4] == "不良-著色不佳":
                        if x <= dis_x and x+w >= dis_x+dis_w and y <= dis_y and y+h >= dis_y+dis_h:
                            f_txt.writelines('3 '+ str(dis_x-x)+ ' ' + str(dis_y-y)+ ' '+ str(dis_w)+' ' + str(dis_h) + '\n')
                    elif disease_list[idx_row+4] == "不良-黑斑病":
                        if x <= dis_x and x+w >= dis_x+dis_w and y <= dis_y and y+h >= dis_y+dis_h:
                            f_txt.writelines('4 '+ str(dis_x-x)+ ' ' + str(dis_y-y)+ ' '+ str(dis_w)+' ' + str(dis_h) + '\n')
                    else:
                        print("sth wrong")
                        print(disease_list[idx_row+4])
                        print(imgname)
                    idx_row += 5
                    if idx_row >= len(disease_list):
                        f_txt.close()
                        break
                    if disease_list[idx_row] == '':
                        f_txt.close()
                        break
                    ###
                arr = []
            start = line.find("/Train/") + 7
            end = line.find(".jpg")
            imgname = line[start:end]
            image = cv2.imread("Train/" + imgname + ".jpg")
        if 'mango:' in line:
            arr.append(line.split())
###store last .jpg file to txt
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
        #write to file
        disease_list = None
        for find_name in f_dis:
            if imgname+".jpg" in find_name:
                disease_list =  find_name.split(',')
                break
        idx_row = 1
        f_txt = open("tempt/" + imgname + ".txt", "w")
        while True:
            dis_x = int(float(disease_list[idx_row]))
            dis_y = int(float(disease_list[idx_row+1]))
            dis_w = int(float(disease_list[idx_row+2]))
            dis_h = int(float(disease_list[idx_row+3]))
            ###
            if "不良-乳汁吸附" in disease_list[idx_row+4] :
                if x <= dis_x and x+w >= dis_x+dis_w and y <= dis_y and y+h >= dis_y+dis_h:
                    f_txt.writelines('0 '+ str(dis_x-x)+ ' ' + str(dis_y-y)+ ' '+ str(dis_w)+' ' + str(dis_h) + '\n')
            elif disease_list[idx_row+4] == "不良-機械傷害":
                if x <= dis_x and x+w >= dis_x+dis_w and y <= dis_y and y+h >= dis_y+dis_h:
                    f_txt.writelines('1 '+ str(dis_x-x)+ ' ' + str(dis_y-y)+ ' '+ str(dis_w)+' ' + str(dis_h) + '\n')
            elif disease_list[idx_row+4] == "不良-炭疽病":
                if x <= dis_x and x+w >= dis_x+dis_w and y <= dis_y and y+h >= dis_y+dis_h:
                    f_txt.writelines('2 '+ str(dis_x-x)+ ' ' + str(dis_y-y)+ ' '+ str(dis_w)+' ' + str(dis_h) + '\n')
            elif disease_list[idx_row+4] == "不良-著色不佳":
                if x <= dis_x and x+w >= dis_x+dis_w and y <= dis_y and y+h >= dis_y+dis_h:
                    f_txt.writelines('3 '+ str(dis_x-x)+ ' ' + str(dis_y-y)+ ' '+ str(dis_w)+' ' + str(dis_h) + '\n')
            elif disease_list[idx_row+4] == "不良-黑斑病":
                if x <= dis_x and x+w >= dis_x+dis_w and y <= dis_y and y+h >= dis_y+dis_h:
                    f_txt.writelines('4 '+ str(dis_x-x)+ ' ' + str(dis_y-y)+ ' '+ str(dis_w)+' ' + str(dis_h) + '\n')
            else:
                print("sth wrong")
            idx_row += 5
            if idx_row >= len(disease_list):
                f_txt.close()
                break
            if disease_list[idx_row] == '':
                f_txt.close()
                break
