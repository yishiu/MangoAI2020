import cv2
# 不良-乳汁吸附 不良-機械傷害 不良-炭疽病 不良-著色不佳 不良-黑斑病


def formatnum(v):
        return "%.6f" % v
flag = 0
with open("train.csv") as f_name:
    for line in f_name:
        arr = line.split()[0].split(',')
        filename = arr[0]
        if flag == 0:
            flag = 1
            filename = filename[1:]
        img = cv2.imread("Train/"+filename)
        filename = filename[:-4]
        i = 1
        f = open("Train/" + filename + ".txt", "w")
        while True :
            x = int(float(arr[i]))
            y = int(float(arr[i+1]))
            box_w = int(float(arr[i+2]))
            box_h = int(float(arr[i+3]))
            height = img.shape[0]
            width = img.shape[1]
            x_cen = int(x + box_w/2)
            y_cen = int(y+box_h/2)
            r = [x_cen/width, y_cen/height, box_w/width, box_h/ height]
            numbers = [formatnum(v) for v in r]
            if arr[i+4] == "不良-乳汁吸附" :
                f.writelines('0 ' + str(numbers[0]) + ' '+ str(numbers[1]) + ' '+ str(numbers[2]) + ' '+ str(numbers[3])+'\n')
            elif arr[i+4] == "不良-機械傷害" :
                f.writelines('1 ' + str(numbers[0]) + ' '+ str(numbers[1]) + ' '+ str(numbers[2]) + ' '+ str(numbers[3])+ '\n')
            elif arr[i+4] == "不良-炭疽病" :
                f.writelines('2 ' + str(numbers[0]) + ' '+ str(numbers[1]) + ' '+ str(numbers[2]) + ' '+ str(numbers[3])+ '\n')
            elif arr[i+4] == "不良-著色不佳" :
                f.writelines('3 ' + str(numbers[0]) + ' '+ str(numbers[1]) + ' '+ str(numbers[2]) + ' '+ str(numbers[3])+ '\n')
            elif arr[i+4] == "不良-黑斑病" :
                f.writelines('4 ' + str(numbers[0]) + ' '+ str(numbers[1]) + ' '+ str(numbers[2]) + ' '+ str(numbers[3])+'\n')
            else:
                print("Wrong reading")
            i = i + 5
            if i >= len(arr):
                f.close()
                break
            if arr[i] == '':
                f.close()
                break

