import tkinter as tk
from tkinter import filedialog
import cv2
import object_detection_tkinter
from PIL import Image, ImageTk
import os


cap = None  

def upload_file():
    global cap
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    if file_path:
        stop_video()
        process_video(file_path)

def callback():
    filename = 'object_detection.py'
    os.system(filename)  

def on_enter(e):
    upload_button.config(bg=button_hover_bg, fg=button_hover_fg)

def on_leave(e):
    upload_button.config(bg=button_bg, fg=button_fg)

def on_realtime_enter(e):
    realtime_button.config(bg=button_hover_bg, fg=button_hover_fg)

def on_realtime_leave(e):
    realtime_button.config(bg=button_bg, fg=button_fg)

def toggle_mode():
    global mode, button_bg, button_fg, button_hover_bg, button_hover_fg
    if mode == "light":
        mode = "dark"
        button_bg = "black"
        button_fg = "white"
        button_hover_bg = "white"
        button_hover_fg = "black"
        root.config(bg="#5E574C")
    else:
        mode = "light"
        button_bg = "blue"
        button_fg = "white"
        button_hover_bg = "red"
        button_hover_fg = "white"
        root.config(bg="#F8F2E8")

def play_video():
    global cap, timer
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = object_detection_tkinter.process_frame(frame)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        video_label.config(image=photo)
        video_label.image = photo
        timer = root.after(30, play_video)  
    else:
        cap.release()

def pause_video():
    root.after_cancel(timer)  

def stop_video():
    global cap
    if cap is not None:
        root.after_cancel(timer) 
        cap.release()
        video_label.config(image=None)  
        cap = None

def process_video(video_path):
    global cap
    cap = cv2.VideoCapture(video_path)
    play_video()


mode = "light"
button_bg = "blue"
button_fg = "white"
button_hover_bg = "red"
button_hover_fg = "white"

root = tk.Tk()
root.title("Video Uploader and Object Detector")
root.geometry("1600x1200")
root.config(bg="white")

text_label = tk.Label(root, text="Pongsapak Jongsomsuk", fg="black")
text_label.pack(pady=2)

upload_button = tk.Button(root, text="Object Detection From File", command=upload_file, bg=button_bg, fg=button_fg, width=20, height=3, bd=3)
upload_button.pack(side=tk.LEFT, padx=10, pady=100)

realtime_button = tk.Button(root, text="Real-time Object Detection", command=callback, bg=button_bg, fg=button_fg, width=20, height=3, bd=3)
realtime_button.pack(side=tk.RIGHT, padx=10, pady=100)

upload_button.bind("<Enter>", on_enter)
upload_button.bind("<Leave>", on_leave)

realtime_button.bind("<Enter>", on_realtime_enter)
realtime_button.bind("<Leave>", on_realtime_leave)

mode_button = tk.Button(root, text="Toggle Mode", command=toggle_mode, bg=button_bg, fg=button_fg, bd=3)
mode_button.pack()

video_label = tk.Label(root)
video_label.pack()

root.mainloop()
