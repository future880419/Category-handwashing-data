from cv2 import cv2 as cv2   # for capturing videos
import matplotlib.pyplot as plt    # for plotting the images 
import shutil
import os
import math   # for mathematical operations
from skimage.transform import resize   # for resizing images
from keras.preprocessing import image   # for preprocessing the images

#  set dir_path
Oringnal_Path="D:\大2功課\python"
Dataset_Path = "D:\大學專題\洗手實做\HandWashDataset\For_train"
Category_Name=["\Step_1","\Step_2_Left","\Step_2_Right","\Step_3","\Step_4_Left","\Step_4_Right",
"\Step_5_Left","\Step_5_Right","\Step_6_Left","\Step_6_Right","\Step_7_Left","\Step_7_Right"]
Traindata_Path="D:\大學專題\洗手實做\Traindata"

#  set frameRate
#  frameRate = cap.get(5) # 原本影片1s ?張
frameRate =1 # 1s 16偵 根據: https://www.itread01.com/content/1546997061.html

#  category information
cut_counter=[]
Video_Path=Dataset_Path+Category_Name[0]
category=0 #3秒為一個訓練資料的count
count = 0 #一個影片的count
One_X_secs = 8 # 16* ?? 秒
all_category_counter=0 #所有類別的影片的count
frame_name=0 
frame_x=0
frame_y=0
frame_w=0
frame_h=0

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

        # one video 單一影片處理
        while(cap.isOpened()):
            frameId = cap.get(1) #current frame number 每一楨
            ret, frame = cap.read()
            if (ret != True):
                break
            if (frameId % math.floor(frameRate) == 0): #frameRate的倍數取一張來讀
               
                #將讀到的frame先剪裁 再resize
                frame_h=frame.shape[0] #frame 的高度
                if(frame.shape[0]<frame.shape[1]):
                    frame_x=int((frame.shape[1]-frame.shape[0])/2) #x start 設在扣掉左邊框後
                    frame_w=frame.shape[0] #x end 設成跟高一樣，變成正方形
                frame = frame[frame_y:frame_y+frame_h, frame_x:frame_x+frame_w] #剪裁
                frame=cv2.resize(frame, (112, 112), interpolation=cv2.INTER_CUBIC)
                
                #製造資料夾類別 從0開始
                if(count%One_X_secs ==0):
                    category=math.floor(count/One_X_secs) 
                    category=all_category_counter+category #上一個影片算完的counter+這次的category
                    folser_path=Traindata_Path+"\%d" % category #set path
                    os.mkdir(folser_path) # make folder
                    os.chdir(folser_path)#shutil.move(filename,path) #跳目錄位置，跳到存放照片的地方
                
                #圖片存取
                frame_name=count-(category-all_category_counter)*One_X_secs #每個類別從0開始
                filename ="frame%d.jpg" %frame_name#set檔名
                cv2.imwrite(filename, frame)    #將照片寫入
                count+=1 #下一張圖片
        cap.release() 
        os.chdir(Oringnal_Path) #跳回原本目錄位置
        
        #delet not full folder
        if(count%One_X_secs !=0):
            delet_folser_path= Traindata_Path+"\%d" % category #set path
            shutil.rmtree(delet_folser_path)
            all_category_counter=category #next time start folder
            print(all_category_counter)#all video 被分成幾個輸入
        #folder is full 48(3s)
        else:
            all_category_counter=category+1
            print(all_category_counter)  #all video 被分成幾個輸入
    print(all_category_counter) #all video 被分成幾個輸入 從 0~ all_category_counter-1
    cut_counter.append(all_category_counter)

#顯示資料夾分段點
print(cut_counter)
os.chdir(Oringnal_Path)  
