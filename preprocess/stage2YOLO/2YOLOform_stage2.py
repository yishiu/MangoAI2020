import cv2
#abc.txt: tempt/XXXXX.txt
def formatnum(v):
    return "%.6f" % v
with open("abc.txt") as f_name:
    for line in f_name:
        filename = line[6:11]
        img = cv2.imread("cut3000yolo_dev/" + filename +".jpg")
        height = img.shape[0]
        width = img.shape[1]
        fout = open("cut3000yolo_dev/" + filename+".txt", "w")
        with open(line[:-1]) as f_dis:
            for disease in f_dis:
                arr = disease.split()
                x = int(arr[1])
                y = int(arr[2])
                box_w = int(arr[3])
                box_h = int(arr[4])
                x_cen = int(x + box_w/2)
                y_cen = int(y + box_h/2)
                r = [ x_cen/width, y_cen/height, box_w/width, box_h/height]
                numbers = [formatnum(v) for v in r]
                fout.writelines(arr[0] +' ' + str(numbers[0]) +' '+ str(numbers[1]) + ' ' + str(numbers[2]) + ' ' + str(numbers[3]) + '\n' )
        fout.close()


