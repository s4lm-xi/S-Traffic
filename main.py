import subprocess as s
import tkinter as tk
from arabic_reshaper import reshape
import os
from bidi.algorithm import get_display
import pandas as pd
import cv2
import pygame

def start(limit):
    path = 'output/output.mp4'
    video = cv2.VideoCapture(path)
    data = pd.read_csv('csv/results.csv')
    index = 0
    do = True
    
    try:
        while True:
            _, frame = video.read()

            cv2.imshow('Stream...', frame)
            if do:
                num = data['number'][index]
                if num == limit:
                    pygame.mixer.init()
                    pygame.mixer.music.load("alert.wav")
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy() == True:
                        continue        
                    s.call(['notify-send', 'تنبيه','تم الوصول الى الحد الاقصى'])
                    do = False
                
                index +=1
            
            if cv2.waitKey(25) == ord('q'):
                cv2.destroyAllWindows()
                video.release()
                break
    except:
        cv2.destroyAllWindows()
        video.release()
        
def graph():
    os.system('xdg-open /home/s4lm_xi/S-Traffic/graphs')

def destroy():
    window.destroy()
    
window = tk.Tk()
window.title('S-Traffic')

emp = tk.Label(window, text='''
███████╗   ████████╗██████╗  █████╗ ███████╗███████╗██╗ ██████╗
██╔════╝   ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██║██╔════╝
███████╗█████╗██║   ██████╔╝███████║█████╗  █████╗  ██║██║     
╚════██║╚════╝██║   ██╔══██╗██╔══██║██╔══╝  ██╔══╝  ██║██║     
███████║      ██║   ██║  ██║██║  ██║██║     ██║     ██║╚██████╗
╚══════╝      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝ ╚═════╝
                                                               
''', fg='red').grid(row=0, column=1, padx=120, pady=30)

lbl = tk.Button(window, text=get_display(reshape('ابدأ المراقبة')), font=('', 19),
               command=lambda: start(scale_widget.get()), borderwidth = 3)
lbl.grid(row=1, column=0)

scale_widget = tk.Scale(window, from_=1, to=100,
                             orient=tk.HORIZONTAL, width=35, borderwidth=2, font=('', 15))
scale_widget.grid(row=1, column=1)

lbl = tk.Button(window, text=get_display(reshape('اوقف المراقبة')), font=('', 19), borderwidth = 3)
lbl.grid(row=1, column=2)

lbl = tk.Button(window, text=get_display(reshape('الخروج')), font=('', 19),
               command=destroy, borderwidth = 3)
lbl.grid(row=2, column=0)

lbl = tk.Button(window, text=get_display(reshape('تحليل البيانات')), font=('', 19),
               command=graph, borderwidth = 3)
lbl.grid(row=2, column=2)

window.mainloop()
