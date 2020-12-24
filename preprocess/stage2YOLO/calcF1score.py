import cv2
# 不良-乳汁吸附 不良-機械傷害 不良-炭疽病 不良-著色不佳 不良-黑斑病
# get label from dev dataset and check f_detect's precision
# calculate five label accuracy
TP = [0, 0, 0, 0, 0]
FP = [0, 0, 0, 0, 0]
FN = [0, 0, 0, 0, 0]
test = 0
#with open("dev.csv") as f_name, open("result_stage2_dev_1thresh.txt") as f_detect :
with open("dev.csv") as f_name, open("result_stage2_dev.txt") as f_detect :
    for i, line in enumerate(f_name):
        #print(i)
        arr = line.split()[0].split(',')
        if i != 0: #BOM in .csv file
            filename = arr[0]
        else:
            filename = arr[0][1:]
        filename = filename[:-4]
        i_row = 1
        count = [0,0,0,0,0]
        while arr[i_row] != '' :
            if "不良-乳汁吸附" in arr[i_row+4]:
                count[0] =  1
            elif arr[i_row+4] == "不良-機械傷害" :
                count[1] =  1
            elif arr[i_row+4] == "不良-炭疽病" :
                count[2] =  1
            elif arr[i_row+4] == "不良-著色不佳" :
                count[3] =  1
            elif arr[i_row+4] == "不良-黑斑病" :
                count[4] =  1
            else:
                print("Wrong reading")
            i_row = i_row + 5
            if i_row >= len(arr):
                break
        f_detect.seek(0)
        find = 0
        findarr = [0, 0, 0, 0, 0]
        for dline in f_detect:
            if ".jpg:" in dline and find == 1:
                find = 0
                for idx in range(5):
                    if count[idx] == 1 and findarr[idx] == 1:
                        TP[idx] += 1
                    elif count[idx] == 0 and findarr[idx] == 1:
                        FP[idx] += 1
                    elif count[idx] == 1 and findarr[idx] == 0:
                        FN[idx] += 1
                break
            if "/"+filename+".jpg:" in dline:
                find = 1
                test += 1
                continue
            if find == 1 and dline.split()[0] == "D0:":
                findarr[0] = 1
            if find == 1 and dline.split()[0] == "D1:":
                findarr[1] = 1
            if find == 1 and dline.split()[0] == "D2:":
                findarr[2] = 1
            if find == 1 and dline.split()[0] == "D3:":
                findarr[3] = 1
            if find == 1 and dline.split()[0] == "D4:":
                findarr[4] = 1
print("==============\nTP")
for i in range(5):
    print(TP[i])
print("==============\nFP")
for i in range(5):
    print(FP[i])
print("==============\nFN")
for i in range(5):
    print(FN[i])
sum_pre = 0.0
sum_recall = 0.0
print("=================\nprecision: ")
for i in range(5):
    print(TP[i]/(TP[i]+FP[i]+0.0000001))
    sum_pre += TP[i]/(TP[i]+FP[i]+0.0000001)
print("==============")
print("recall: ")
for i in range(5):
    print(TP[i]/(TP[i]+FN[i]+0.00000001))
    sum_recall += TP[i]/(TP[i]+FN[i]+0.00000001)
print("==============")
print("F1 score")
print( (sum_pre/5*sum_recall/5)/(sum_pre/5 + sum_recall/5) *2)
print("test")
print(test)
