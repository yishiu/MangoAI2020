import numpy as np
import cv2
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import pandas as pd
from torch.utils.data import DataLoader, Dataset
import time
import os
from model import Classifier
from dataset import ImgDataset
import argparse
def loadmodel(model, name):
    print("restore model")
    model.load_state_dict(torch.load(name, map_location = 'cpu'))

def readfile(path, label):
    image_dir = sorted(os.listdir(path))
    x = np.zeros((len(image_dir), 128, 128, 3), dtype=np.uint8)
    y = np.zeros((len(image_dir)), dtype=np.uint8)
    for i, file in enumerate(image_dir):
        img = cv2.imread(os.path.join(path, file))
        x[i, :, :] = cv2.resize(img,(128, 128))
        if label:
          y[i] = int((file.split("D")[1])[0]) #get the training label(0-10)
    if label:
      return x, y
    else:
      return x
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', required = True)
    args = parser.parse_args()
    workspace_dir = './sickmango'
    batch_size = 64
    test_transform = transforms.Compose([
        transforms.ToPILImage(),
        #transforms.RandomResizedCrop(224),                          
        transforms.ToTensor(), #covert PLI or ndarray to torch.Tensor
    ])

    val_x, val_y = readfile(os.path.join(workspace_dir, "Dev"), True)
    val_set = ImgDataset(val_x, val_y, test_transform)
    val_loader = DataLoader(val_set, batch_size, shuffle=False)
    model = Classifier().cuda()
    loadmodel(model, args.w)
    model.eval()
    prediction = []
    all_pred = []
    with torch.no_grad():
        for i, data in enumerate(val_loader):
            test_pred = model(data[0].cuda())
            test_label = np.argmax(test_pred.cpu().data.numpy(), axis=1)
            for y in test_label:
                prediction.append(y)
            for y in test_pred.cpu().data.numpy():
                all_pred.append(y)

    with open("predict.csv", 'w') as f:
        #f.write('Id,Category\n')
        for i, y in  enumerate(prediction):
            f.write('{},{}\n'.format(i, y))
    with open("allpredict.csv", 'w') as f:
        #f.write('Id,Category\n')
        for i, y in  enumerate(all_pred):
            f.write(str(y)+ '\n')
