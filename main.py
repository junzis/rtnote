import numpy as np
import simpleaudio as sa
import tkinter as tk
import wave
import matplotlib
from easygui import fileopenbox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


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

    def update_signal(self):
        fig = Figure(figsize=(10, 3))
        p = fig.add_subplot(111)
        p.plot(self.signal)
        self.canvas = FigureCanvasTkAgg(fig, master=self.uiroot)
        self.canvas.get_tk_widget().place(x=10, y=80)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.uiroot)
        self.toolbar.update()

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
            self.btn_play.config(text="Play")
        else:
            self.player = self.wave.play()
            self.btn_play.config(text="Stop")


if __name__ == "__main__":
    ui = MainUI()
    ui.start()