# HESAI Pandar XT32 Point Cloud Data Acquirement

Date: 							2023.03.04

Name:  						ChangMin An

Student Number:   	21700421

Github: 						[Link](https://github.com/ckdals915/DLIP.git)

Demo Video: 		  	[Link](https://youtu.be/UxfRx_APDns)



## I. Introduction

**Goal: HESAI Pandar XT32 LiDAR Acquirement Point Cloud Data using python**

HESAI에서 제공하는 라이다 데이터를 취득하는 [SDK](https://github.com/HesaiTechnology/HesaiLidar_General_SDK)의 경우 Ubuntu에서 C++ 환경에서 얻을 수 있다. 그렇기에 windows, python 환경에서 포인트 클라우드 데이터를 얻는데에  어려움이 있었다. 이 코드는 windows 환경에서 python 언어로 HESAI XT-32 LiDAR의 Point Cloud Data를 얻을 수 있다. 센서의 데이터 획득 속도인 10Hz를 유지하기 위해  python의 multiprocessing 모듈을 이용하여 데이터를 unpack하고 visualization하는 것을 목표로 두고 있다. 

**References:**

* [HESAI Pandar XT32 User Manual](https://github.com/ckdals915/2022_LiDARSimulation_ChangMinAn/blob/main/Hardware/HESAI_Pandar_XT32/XT32_User_Manual.pdf)



## II. Requirement

### Hardware

* HESAI Pandar XT32

### Software

* Python 3.9.12



## III. Installation

### 1. Install Anaconda

**Anaconda** : Python and libraries package installer.

Follow: [How to install Anaconda](https://ykkim.gitbook.io/dlip/installation-guide/anaconda#conda-installation)



### 2. Install Python

> Python 3.8

Python is already installed by installing Anaconda. But, we will make a virtual environment for a specific Python versionn.

* Open Anaconda Prompt(admin mode)<img src="Images/conda.jpg" style="zoom:50%;" />

  

* First, update conda

```
conda update -n base -c defaults conda
```

<img src="Images/conda2.jpg" style="zoom:50%;" />



* Then, Create virtual environment for Python 3.8. Name the $ENV as `XT32_py38`. If you are in base, enter `conda activate XT32_py38`

```
conda create -n XT32_py38 python=3.8.16
```

<img src="Images/conda3.jpg" style="zoom:50%;" />



* After installation, activate the newly created environment

```
conda activate XT32_py38
```

<img src="Images/conda4.jpg" style="zoom:50%;" />



### 3. Install Libs

**Install Numpy, OpenCV, Matplot, Jupyter**

```
conda activate XT32_py38
conda install -c anaconda seaborn jupyter
python -m pip install --upgrade pip
pip install opencv-python
```



### 4. Install Visual Studio Code

Follow: [How to Install VS Code](https://ykkim.gitbook.io/dlip/installation-guide/ide/vscode#installation)

Also, read about [How to program Python in VS Code](https://ykkim.gitbook.io/dlip/installation-guide/ide/vscode/python-vscode)



## IV. Flow Chart

<img src="images/flowchart.jpg" style="zoom:90%;" />



## V. Procedure



### 1. Connect Sensor

#### 1-1. Connect LiDAR sensor through Ethernet cable

<img src="Images/connection.jpg" style="zoom:50%;" />



#### 1-2. Ethernet Configuration

##### 1-2-1. Open the Network Sharing Center, click on "Ethernet"

<img src="Images/Ethernet1.jpg" style="zoom:50%;" /><img src="Images/Ethernet2.jpg" style="zoom:30%;" />



##### 1-2-2. In the "Ethernet Status" box, click on "Properties"



 <img src="Images/Ethernet3.jpg" style="zoom:50%;" /><img src="Images/Ethernet4.jpg" style="zoom:50%;" />



##### 1-2-3. Double-click on "Internet Protocol Version 4 (TCP/IPv4)"

<img src="Images/Ethernet5.jpg" style="zoom:50%;" />

##### 1-2-4. Configure the IP address to 192.168.1.100 and subnet mask to 255.255.255.0

<img src="Images/Ethernet6.jpg" style="zoom:50%;" />



##### 1-2-5. Check that LiDAR is connected (Search 192.168.1.201 in search bar)

<img src="Images/verification.jpg" style="zoom:50%;" />

### 2. Download code





## VII. Demo Video

[Click Demo Video](https://youtu.be/UxfRx_APDns)



## VIII. Conclusion

In this experiment, object detection is implemented using the pretrained model provided by YOLO V5. Through this, it is possible to draw the bounding box of each object, and the number of detected cars can be determined. Through this, it is possible to immediately analyze the parking space of the car, and through this, it is possible to expect to prevent a crowded situation in the parking lot. It can be seen that improvement should be made through appropriate model selection and additional learning for each situation.



## IX. Appendix

### main.py

```python
'''
* *****************************************************************************
* @author	ChangMin An
* @Mod		2022 - 05 - 24
* @brief	DLIP LAB: Parking Management System
* @Version	Python 3.9.12, CUDA 11.3.1(RTX 3060 Laptop), pytorch 1.10 
* *****************************************************************************
'''

#===============================================#
#              Open Library Declare             #
#===============================================#
import torch
import cv2 as cv
from matplotlib import pyplot as plt
from cv2 import *
from cv2.cv2 import *
import random
from PIL import Image
import numpy as np

#===============================================#
#                Global Variable                #
#===============================================#
# Video Variable
Video = "DLIP_parking_test_video.avi"

# Color Definition (BGR)
WHITE               = (255, 255, 255)
RED                 = (  0,   0, 255)
GREEN               = (  0, 255,   0)
PINK                = (184,  53, 255)
YELLOW              = (  0, 255, 255)
BLUE                = (255,   0,   0)
BLACK               = (  0,   0,   0)
PURPLE              = (255, 102, 102)

# Font Definition
USER_FONT           = FONT_HERSHEY_DUPLEX
TRANSPARENCY        = 0.3

# Variable about Parking Point 
center_Point = []
parking_Point = [(78,378),(175,380),(289,379),(384,379),(490,378),(580,378),(690,378),					 (774,376),(885,376),(977,373),(1084,373),(1179,373),(1260,336)]
parking_Coordinate = [[(70,325),(175,325),(85,430),(0,430)],
                      [(175,325),(265,325),(200,430),(85,430)],
                      [(265,325),(360,325),(312,430),(200,430)],
                      [(360,325),(454,325),(423,430),(313,430)],
                      [(454,325),(546,325),(527,430),(423,430)],
                      [(546,325),(635,325),(635,430),(527,430)],
                      [(635,325),(720,325),(747,430),(635,430)],
                      [(720,325),(810,325),(850,430),(747,430)],
                      [(810,325),(900,325),(956,430),(850,430)],
                      [(900,325),(990,325),(1065,430),(956,430)],
                      [(990,325),(1080,325),(1175,430),(1065,430)],
                      [(1080,325),(1165,325),(1280,430),(1175,430)],
                      [(1165,325),(1280,300),(1280,400),(1280,430)]]
parking_Flag = [False,False,False,False,False,False,False,False,False,False,False,False,False]

# Frame Text Variable
frame_Num = 0

# Open the File
f = open("counting_result.txt",'w')
f.write("Frame\tNumber of Car\n")

#===============================================#
#                     Main                      #
#===============================================#

# Load the Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5m6', pretrained=True)

# Threshold Configuration
model.conf = 0.1

# Open the Video & Recording Video Configuration
cap = cv.VideoCapture(Video)
w = round(cap.get(CAP_PROP_FRAME_WIDTH))
h = round(cap.get(CAP_PROP_FRAME_HEIGHT))
fps = cap.get(CAP_PROP_FPS)
fourcc = VideoWriter_fourcc(*'DIVX')
out = VideoWriter('output.avi', fourcc, fps, (w,h))
delay = round(1000/fps)

if (cap.isOpened() == False):
  print("Not Open the VIDEO")

#================== While Loop =================#    
while(1):
  # Start Window Time
  startTime = cv.getTickCount()

  # Initialization
  car_Count = 0
  parking_Flag =[False,False,False,False,False,False,False,False,False,False,False,False,False]
  
  # Read Video Capture
  cap_Flag, src = cap.read()

  # If Capture is failed, break the loop
  if cap_Flag == False:
    print("Video End")
    break
  
  # Pre-Processing
  src_gray = cvtColor(src, cv.COLOR_BGR2GRAY)
  src_filtered = GaussianBlur(src_gray, (5,5), 0)
  
  # ROI Setting
  roi = np.zeros_like(src_filtered)
  src_roi = np.zeros_like(src_filtered)
  roi_point = np.array([[60,280], [1280,280], [1280,430], [0, 440]])
  roi = fillConvexPoly(roi, roi_point, WHITE)
  bitwise_and(src_filtered, src_filtered, src_roi, roi)

  # Run Inference
  results = model(src_roi)

  # Calculate the Bounding Box result using Pandas
  L_xyxy = len(results.pandas().xyxy[0])
  for i in range(L_xyxy):
    # X, Y Coordinate Value
    Xmin = round(results.pandas().xyxy[0].xmin[i])
    Xmax = round(results.pandas().xyxy[0].xmax[i])
    Ymin = round(results.pandas().xyxy[0].ymin[i])
    Ymax = round(results.pandas().xyxy[0].ymax[i])

    # Class: Car, Bus, Truck
    if results.pandas().xyxy[0].name[i] == "car" or
       results.pandas().xyxy[0].name[i] == "truck" or
       results.pandas().xyxy[0].name[i] == "bus":
      for j in range(len(parking_Point)):
        # Parking Position about X,Y & Parking Flag is false
        if parking_Point[j][0] > Xmin and
        parking_Point[j][0] < Xmax and parking_Point[j][1] > Ymin and
        parking_Point[j][1] < Ymax and parking_Flag[j] == False:
            parking_Flag[j] = True
            car_Count += 1
            cv.rectangle(src, (Xmin, Ymin), (Xmax, Ymax), RED, 2)
            break
    else:
      continue

  # When it is available parking space, Draw parking area to green
  for i in range(len(parking_Flag)):
    if parking_Flag[i] == False:
      parking_Array = np.array([[parking_Coordinate[i][0]],[parking_Coordinate[i][1]],									[parking_Coordinate[i][2]],[parking_Coordinate[i][3]]])
      mask = src.copy()
      cv.fillConvexPoly(src, parking_Array, GREEN)
      src = addWeighted(src, 1-TRANSPARENCY, mask, TRANSPARENCY, gamma=0)

  # Press Esc to Exit, Stop Video to 's' 
  k = cv.waitKey(delay) & 0xFF
  if k == 27:
    break
  elif k == ord('s'):
    cv.waitKey()
  
  # Count Text
  Count_Text = f"Number of Car: {car_Count}"
  putText(src, Count_Text, (100, 120), USER_FONT, 1, RED)

  # Write the Parking Count at Text File
  f.write(f"{' '*3}{frame_Num}\t{' '*7}{car_Count}\n")
  
  # Update
  frame_Num += 1

  # Time Loop End
  endTime = cv.getTickCount()

  # FPS Calculate
  FPS = round(getTickFrequency()/(endTime - startTime))

  # FPS Text
  FPS_Text = f"FPS: {FPS}"
  putText(src, FPS_Text, (100, 160), USER_FONT, 1, RED)

  # Show result image
  imshow("source", src)

  # Record Video
  out.write(src)

# Release
cv.destroyAllWindows()
cap.release()
out.release()
f.close()
```



