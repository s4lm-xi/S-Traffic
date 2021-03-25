import cv2
import os
from skimage.transform import resize 
import os
import glob

video = cv2.VideoCapture('input/input.mp4')
check = len(os.listdir('frames/'))
index = 0

if check > 0:
    # Delete all the frames
    files = glob.glob('frames/*')
    for f in files:
        os.remove(f)
    
while True:
    _, frame = video.read()
    
    try:
        res = resize(frame, (576,1024))
        
        cv2.imwrite(f'frames/{index}.jpg', res*255)
        index +=1
    except:
        print('Done!')
        print(f'Extracted {index} frames')
        print(res.shape)
        break
