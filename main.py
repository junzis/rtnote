import numpy as np
import simpleaudio as sa
import tkinter as tk
import wave
import time
import threading
from easygui import fileopenbox


class MainUI(object):
    def __init__(self):
        self.data = []

        self.file = None
        self.player = None
        self.wave = None

        self.uiroot = tk.Tk()
        self.populate_ui()

    def populate_ui(self):
        self.uiroot.protocol("WM_DELETE_WINDOW", self.shutdown)
        self.uiroot.minsize(300, 300)
        self.uiroot.geometry("1000x500")
        self.uiroot.wm_title("ATC audio player")

        self.btn_open = tk.Button(self.uiroot, text="Open", command=self.open_audio)
        self.btn_open.place(x=10, y=10)

        self.btn_play = tk.Button(self.uiroot, text="Play", command=self.toggle_audio)
        self.btn_play.place(x=80, y=10)

        t1 = threading.Thread(target=self.check_audio)
        t1.setDaemon(True)
        t1.start()

        # self.update_signal()

    def update_signal(self):

        cw = 980
        ch = 200
        self.canvas = tk.Canvas(self.uiroot, bg="white", width=cw, height=ch)

        y = self.signal
        n = len(y)
        y = y / max(y) * ch * 0.3 + ch / 2

        x = np.linspace(0, cw, n)

        coords = np.zeros(n * 2)
        coords[::2] = x
        coords[1::2] = y

        self.canvas.create_line(*coords)

        self.canvas.place(x=10, y=80)

    def start(self):
        self.uiroot.mainloop()

    def shutdown(self):
        self.uiroot.destroy()
        self.uiroot.quit()

    def open_audio(self):

        self.file = fileopenbox()
        print("selected audio: ", self.file)

        self.wave = sa.WaveObject.from_wave_file(self.file)
        sample_rate = self.wave.sample_rate
        num_channels = self.wave.num_channels
        print("Number of channels: ", num_channels)
        print("Sample rate: ", sample_rate)

        self.signal = np.frombuffer(
            wave.open(self.file, "r").readframes(-1), dtype="int16"
        )
        self.update_signal()

    def toggle_audio(self):
        print("toggle playing audio: ", self.file)

        if self.player and self.player.is_playing():
            self.player.stop()
        else:
            self.player = self.wave.play()

    def check_audio(self):
        while True:
            if self.player and self.player.is_playing():
                self.btn_play.config(text="Stop")
            else:
                self.btn_play.config(text="Play")
            time.sleep(0.2)


if __name__ == "__main__":
    ui = MainUI()
    ui.start()