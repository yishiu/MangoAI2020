import cv2
# 不良-乳汁吸附 不良-機械傷害 不良-炭疽病 不良-著色不佳 不良-黑斑病
#read train.csv and crop out features to 5 folders
debugline = 0
with open("train.csv") as f_name:
    for i, line in enumerate(f_name):
        arr = line.split()[0].split(',')
        if i != 0:
            filename = arr[0]
        else:
            filename = arr[0][1:]
        img = cv2.imread("Train/"+filename)
        filename = filename[:-4]
        i = 1
        count = [0,0,0,0,0]
        if len(arr) != 136:
            debugline = debugline+1
        while arr[i] != '' :
            crop = img[int(float(arr[i+1])): int(float(arr[i+1])) + int(float(arr[i+3])) , int(float(arr[i])) : int(float(arr[i])) + int(float(arr[i+2]))]
            if arr[i+4] == "不良-乳汁吸附" :
                cv2.imwrite("D0/"+filename+"_"+ str(count[0])+"D0.jpg", crop)
                count[0] = count[0] + 1
            elif arr[i+4] == "不良-機械傷害" :
                cv2.imwrite("D1/"+filename+"_"+ str(count[1])+"D1.jpg", crop)
                count[1] = count[1] + 1
            elif arr[i+4] == "不良-炭疽病" :
                cv2.imwrite("D2/"+filename+"_"+ str(count[2])+"D2.jpg", crop)
                count[2] = count[2] + 1
            elif arr[i+4] == "不良-著色不佳" :
                cv2.imwrite("D3/"+filename+"_"+ str(count[3])+"D3.jpg", crop)
                count[3] = count[3] + 1
            elif arr[i+4] == "不良-黑斑病" :
                cv2.imwrite("D4/"+filename+"_"+ str(count[4])+"D4.jpg", crop)
                count[4] = count[4] + 1
            else:
                print("Wrong reading")
            i = i + 5
            if i >= len(arr):
                break
print("debugline : {}".format(debugline))
