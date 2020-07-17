from cv2 import cv2 as cv2   # for capturing videos 
import math   # for mathematical operations
import matplotlib.pyplot as plt    # for plotting the images
#matplotlib inline
import pandas as pd
from keras.preprocessing import image   # for preprocessing the images
import numpy as np    # for mathematical operations
from keras.utils import np_utils
from skimage.transform import resize   # for resizing images
import shutil
import os
from sklearn.model_selection import train_test_split
Path="D:\大學專題\洗手實做\Traindata"
OringnalPath="D:\大2功課\python"
total_video=10012
One_X_secs = 8
Merge_One_X_secs = One_X_secs*2

# 初始化x
X_train_notran=[[0]*One_X_secs for i in range(total_video)]
x_train=[[0]*Merge_One_X_secs for i in range(total_video-1)]
Merge_x_train=[[0]*Merge_One_X_secs for i in range(total_video-1)]

# read img from correct_path 
for category in range(0,total_video,1):
    #print(category)
    correct_path=Path+"\%d" % category
    os.chdir(correct_path)#shutil.move(filename,path) #跳目錄位置，跳到存放照片的地方
    for number in range(0,One_X_secs,1):
        filename ="frame%d.jpg" % number#set檔名  
        X_train_notran[category][number]= cv2.imread(filename)
    if(category>0):
        Merge_x_train[category-1]=np.concatenate((X_train_notran[category], X_train_notran[category-1]))

# set x to numpy and see shape
X_train_notran=np.array(X_train_notran)
Merge_x_train=np.array(Merge_x_train)
print(X_train_notran.shape)
print(Merge_x_train.shape)  

# 初始化y 並隨機打亂y
y_train =np.array(range(0,total_video-1,1)) #設置每個x的編號
np.random.shuffle(y_train) #random y number

# random x data
for i in range(0,total_video-1,1):
    x_train[i]=Merge_x_train[y_train[i]] #隨機打亂合併後的x，並放在x_train
X_train=np.array(x_train)
print(X_train.shape) 

# set y data 
for i in range(0,total_video-1,1):
    if(y_train[i]>=9318):
        y_train[i]=11
    elif(y_train[i]>=8625 and y_train[i]<9318):
        y_train[i]=10
    elif(y_train[i]>=7898 and y_train[i]<8625):
        y_train[i]=9
    elif(y_train[i]>=7114 and y_train[i]<7898):
        y_train[i]=8
    elif(y_train[i]>=6270 and y_train[i]<7114):
        y_train[i]=7
    elif(y_train[i]>=5433 and y_train[i]<6270):
        y_train[i]=6
    elif(y_train[i]>=4565 and y_train[i]<5433):
        y_train[i]=5
    elif(y_train[i]>=3645 and y_train[i]<4565):
        y_train[i]=4
    elif(y_train[i]>=2759 and y_train[i]<3645):
        y_train[i]=3
    elif(y_train[i]>=1895 and y_train[i]<2759):
        y_train[i]=2
    elif(y_train[i]>=1018 and y_train[i]<1895):
        y_train[i]=1
    else:
        y_train[i]=0

# preparing the validation set
#X_train, X_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.3, random_state=42)    # preparing the validation set
#print(X_train.shape)
#print(X_valid.shape)
print(y_train)
#print(y_valid)

#save data in "D:\大2功課\python"
os.chdir(OringnalPath)
np.save('my_X_train', X_train)
#np.save('my_X_valid', X_train)
np.save('my_y_train', y_train)
#np.save('my_y_valid', y_train)



'''
img =x_train[0][0]
print(img.shape)
cv2.imshow('My Image', img)
cv2.waitKey(0)                #持續等待至使用者按下按鍵為止（單位為毫秒）              
cv2.destroyAllWindows()       #關閉所有視窗
cv2.destroyWindow('My Image') #關閉My Image視窗
'''
'''
count = 0
cam = cv2.VideoCapture(0)
while True:
    ret, img = cam.read()
    vis = img.copy()
    cv2.imshow('Camera', vis)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
'''
