import cv2
def formatnum(v):
    return "%.6f" % v
with open("train.csv") as f_name:
    for i, line in enumerate(f_name):
        arr = line.split()[0].split(',')
        filename = arr[0][:-4]
        x = int(arr[2])
        y = int(arr[3])
        box_w = int(arr[4])
        box_h = int(arr[5])
        img = cv2.imread("Train/" + filename +".jpg")
        height = img.shape[0]
        width = img.shape[1]
        x_cen = int(x + box_w/2)
        y_cen = int(y + box_h/2)
        f = open("Train/" + filename+".txt", "w")
        r = [ x_cen/width, y_cen/height, box_w/width, box_h/height]
        numbers = [formatnum(v) for v in r]
        f.write('0 ' + str(numbers[0]) +' '+ str(numbers[1]) + ' ' + str(numbers[2]) + ' ' + str(numbers[3]) )
