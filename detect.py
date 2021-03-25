import os
import re
import cv2 # opencv library
import numpy as np
from os.path import isfile, join
import matplotlib.pyplot as plt
from tqdm import tqdm
import glob

files = glob.glob('output_frames/*')
for f in files:
    os.remove(f)


# get file names of the frames
col_frames = os.listdir('frames/')

# sort file names
col_frames.sort(key=lambda f: int(re.sub('\D', '', f)))

# empty list to store the frames
col_images=[]

for i in col_frames:
    # read the frames
    img = cv2.imread('frames/'+i)
    # append the frames to the list
    col_images.append(img)



# kernel for image dilation
kernel = np.ones((4,4),np.uint8)

# font style
font = cv2.FONT_HERSHEY_SIMPLEX

# directory to save the ouput frames
pathIn = "output_frames/"

for i in tqdm(range(len(col_images)-1)):
    
    # frame differencing
    grayA = cv2.cvtColor(col_images[i], cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(col_images[i+1], cv2.COLOR_BGR2GRAY)
    diff_image = cv2.absdiff(grayB, grayA)
    
    # image thresholding
    ret, thresh = cv2.threshold(diff_image, 30, 255, cv2.THRESH_BINARY)
    
    # image dilation
    dilated = cv2.dilate(thresh,kernel,iterations = 1)
    
    # find contours
    contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    # shortlist contours appearing in the detection zone
    valid_cntrs = []
    for cntr in contours:
        x,y,w,h = cv2.boundingRect(cntr)
        if (x <= 200*4) & (y >= 50*4) & (cv2.contourArea(cntr) >= 25*4):
            if (y >= 90*4) & (cv2.contourArea(cntr) < 40*4):
                break
            valid_cntrs.append(cntr)
            
    # add contours to original frames
    dmy = col_images[i].copy()
    cv2.drawContours(dmy, valid_cntrs*4, -1, (127,200,0), 2)
    
    cv2.putText(dmy, "vehicles detected: " + str(len(valid_cntrs)), (55*4, 15*8), font, 2, (0, 180, 0), 2)
    cv2.line(dmy, (0, 50),(1024,50),(100, 255, 255))
    cv2.imwrite(pathIn+str(i)+'.png',dmy)  



fps = 30
path = 'output_frames/'
name = 'output.mp4'
img_file = [path+str(i)+'.png' for i in range(len(os.listdir(path)))]
img = cv2.imread(img_file[0])
height, width, channel = img.shape

video = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))
print('Converting..')

for image in tqdm(img_file):
    video.write(cv2.imread(image))

cv2.destroyAllWindows()
video.release()