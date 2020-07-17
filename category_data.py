from cv2 import cv2 as cv2   # for capturing videos
import matplotlib.pyplot as plt    # for plotting the images 
import shutil
import os
import math   # for mathematical operations
from skimage.transform import resize   # for resizing images
from keras.preprocessing import image   # for preprocessing the images
#  set dir_path
Traindata_Path="D:\大學專題\洗手實做\Traindata"
Oringnal_Path="D:\大2功課\python"
Dataset_Path = "D:\大學專題\洗手實做\HandWashDataset\For_train"
Category_Name=["\Step_1","\Step_2_Left","\Step_2_Right","\Step_3","\Step_4_Left","\Step_4_Right",
"\Step_5_Left","\Step_5_Right","\Step_6_Left","\Step_6_Right","\Step_7_Left","\Step_7_Right"]
cut_counter=[]
Video_Path=Dataset_Path+Category_Name[0]

#  set frameRate
    #  frameRate = cap.get(5) # 原本影片1s ?張
frameRate =1 # 1s 16偵 根據: https://www.itread01.com/content/1546997061.html
category=0 #3秒為一個訓練資料的count
count = 0 #一個影片的count
One_X_secs = 8 # 16* ?? 秒
all_category_counter=0 #所有類別的影片的count
frame_name=0 
# read every Category_name 先設類別
for name in Category_Name:
    Video_Path=Dataset_Path+name
    Video_files= os.listdir(Video_Path) #得到資料夾下的所有檔名稱

    # cut up for each video 在設類別下的影片
    for file in Video_files: #遍歷資料夾
        file=Video_Path+ "\%s" % file #set path
        print(file)
        cap = cv2.VideoCapture(file)
        count = 0
        while(cap.isOpened()):
            frameId = cap.get(1) #current frame number 每一楨
            ret, frame = cap.read()
            if (ret != True):
                break
            if (frameId % math.floor(frameRate) == 0): #frameRate的倍數取一張來讀
                frame=cv2.resize(frame, (112, 112), interpolation=cv2.INTER_CUBIC) #將讀到的frame resize
                if(count%One_X_secs ==0):
                    category=math.floor(count/One_X_secs) #判斷類別 從0開始
                    category=all_category_counter+category #上一個影片算完的counter+這次的category
                    folser_path=Traindata_Path+"\%d" % category #set path
                    os.mkdir(folser_path) # make folder
                    os.chdir(folser_path)#shutil.move(filename,path) #跳目錄位置，跳到存放照片的地方
                frame_name=count-(category-all_category_counter)*One_X_secs #每個類別從0開始
                filename ="frame%d.jpg" %frame_name#set檔名
                cv2.imwrite(filename, frame)    #將照片寫入
                count+=1
        cap.release() 
        os.chdir(Oringnal_Path) #跳回原本目錄位置
        if(count%One_X_secs !=0): #delet not full folder
            delet_folser_path= "D:\\大學專題\\洗手實做\\Traindata\\%d" % category  
            shutil.rmtree(delet_folser_path)
            all_category_counter=category #next time start folder
            print(all_category_counter)#all video 被分成幾個輸入
        else:#folder is full 48(3s)
            all_category_counter=category+1
            print(all_category_counter)  #all video 被分成幾個輸入
    print(all_category_counter) #all video 被分成幾個輸入 從 0~ all_category_counter-1
    cut_counter.append(all_category_counter)
print(cut_counter)
os.chdir(Oringnal_Path)  
