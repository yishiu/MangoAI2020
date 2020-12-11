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
def savemodel(model, path, epoch):
    f = os.path.join(path, 'checkpoint-{:06d}'.format(epoch))
    torch.save(model.state_dict(), f)
    print("saved model")
if __name__ == '__main__':
    #data augmentation
    train_transform = transforms.Compose([
        transforms.ToPILImage(), #PIL : python image library
        #transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(), # 隨機將圖片水平翻轉
        transforms.RandomRotation(15), # 隨機旋轉圖片
        transforms.ToTensor(), # 將圖片轉成 Tensor，並把數值 normalize 到 [0,1] (data normalization)
    ])
    test_transform = transforms.Compose([
        transforms.ToPILImage(),          
        #transforms.RandomResizedCrop(224),                          
        transforms.ToTensor(), #covert PLI or ndarray to torch.Tensor
    ])
    #read train set, dev set 
    workspace_dir = './sickmango'
    print("Reading data")
    train_x, train_y = readfile(os.path.join(workspace_dir, "Train"), True)
    print("Size of training data = {}".format(len(train_x)))
    print("label Size of training data = {}".format(len(train_y)))
    val_x, val_y = readfile(os.path.join(workspace_dir, "Dev"), True)
    print("Size of validation data = {}".format(len(val_x)))
    print(train_x.shape)

    #ensure every time has same dataset
    torch.manual_seed(567)
    torch.cuda.manual_seed(567)
    np.random.seed(567)

    #data augmentation & load
    batch_size = 64
    train_set = ImgDataset(train_x, train_y, train_transform)
    val_set = ImgDataset(val_x, val_y, test_transform)
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False)


    model = Classifier().cuda()
    loss = nn.CrossEntropyLoss() # 因為是 classification task，所以 loss 使用 CrossEntropyLoss
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001) # optimizer 使用 Adam
    #num_epoch = 60
    num_epoch = 1
    for epoch in range(num_epoch):
        epoch_start_time = time.time()
        train_acc = 0.0
        train_loss = 0.0
        val_acc = 0.0
        val_loss = 0.0

        model.train() # 確保 model 是在 train model (開啟 Dropout 等...)
        ## for loop train_loder gives out 128 datas "data[0]: training data shape [128, 3, 128, 128] or [batch_size, channel, width, height]", "data[1]: testing data shape[128]"
        for i, data in enumerate(train_loader):
            optimizer.zero_grad() # 用 optimizer 將 model 參數的 gradient 歸零
            train_pred = model(data[0].cuda()) # call model 的 forward 函數 #input of model is (batch_size, input_size_of_network), output is (batch_size, class_dimen)
            #train_pred.shape == [128, 11]
            batch_loss = loss(train_pred, data[1].cuda()) # 計算 loss （注意 prediction 跟 label 必須同時在 CPU 或是 GPU 上）(argument [prediction, y'])
            batch_loss.backward() # 利用 back propagation 算出每個參數的 gradient
            optimizer.step() # 以 optimizer 用 gradient 更新參數值

            train_acc += np.sum(np.argmax(train_pred.cpu().data.numpy(), axis=1) == data[1].numpy()) #find max of 11 class and compare with the train label
            #if i == 1:
            #  print(data[1])
            train_loss += batch_loss.item()  # type(batch_loss) == torch.Tensor

        model.eval()   #same as model.train(False)
        with torch.no_grad():
            for i, data in enumerate(val_loader):
                val_pred = model(data[0].cuda())
                batch_loss = loss(val_pred, data[1].cuda())

                val_acc += np.sum(np.argmax(val_pred.cpu().data.numpy(), axis=1) == data[1].numpy())
                val_loss += batch_loss.item()

            print('[%03d/%03d] %2.2f sec(s) Train Acc: %3.6f Loss: %3.6f | Val Acc: %3.6f loss: %3.6f' % \
                (epoch + 1, num_epoch, time.time()-epoch_start_time, \
                 train_acc/train_set.__len__(), train_loss/train_set.__len__(), val_acc/val_set.__len__(), val_loss/val_set.__len__()))
    savemodel(model, "./", 1)
'''
    #torch.save({'state_dict': model.state_dict()}, 'hw3_parm_b.pkl')
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
'''
