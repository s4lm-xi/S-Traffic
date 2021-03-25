import subprocess as s
import tkinter as tk

window = tk.Tk()
window.title('E-Teacher')

canvas = tk.Canvas(window, width = 300, height = 300)      
canvas.pack()      
img = tk.PhotoImage(file="logo.png")      
canvas.create_image(20,20, anchor=tk.NW, image=img)      

window.mainloop()
