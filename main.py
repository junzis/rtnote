from pydub import AudioSegment
from pydub.playback import play

import tkinter as tk
from easygui import fileopenbox

file = None


def open_audio():
    global file
    file = fileopenbox()
    print("selected audio: ", file)


def toggle_audio():
    global file
    print("playing audio: ", file)
    rec = AudioSegment.from_mp3(file)
    play(rec)
    print("finish playing audio: ", file)


def shutdown():
    root.destroy()
    root.quit()


root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", shutdown)
root.minsize(300, 300)
root.geometry("500x500")
root.wm_title("ATC audio player")

btn_open = tk.Button(root, text="Open", command=open_audio)
btn_open.pack()

btn_play = tk.Button(root, text="Play", command=toggle_audio)
btn_play.pack()


root.mainloop()
