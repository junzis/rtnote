import numpy as np
import simpleaudio as sa
import soundfile as sf
import tkinter as tk
import wave
import time
import threading
from easygui import fileopenbox

canvas_width = 980
canvas_height = 200


class MainUI(object):
    def __init__(self):
        self.data = []

        self.file = None
        self.player = None
        self.audio = None
        self.segment = None

        self.uiroot = tk.Tk()
        self.select = None  # canvas selection object

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

        # load test audio, save time
        self.open_audio("samples/rec-1.wav")

    def update_canvas(self):
        def mouse_down(event):
            self.selection_start = event.x

        def mouse_drag(event):
            self.selection_end = event.x

            if self.select:
                self.canvas.delete(self.select)

            self.select = self.canvas.create_rectangle(
                self.selection_start,
                1,
                event.x,
                canvas_height,
                fill="green",
                outline="black",
                stipple="gray50",
            )

        def mouse_up(event):
            self.selection_end = event.x
            print(self.selection_start, self.selection_end)

            if self.selection_end == self.selection_start:
                if self.select:
                    self.canvas.delete(self.select)
                self.segment = None

            else:
                s0 = min(self.selection_start, self.selection_end)
                s1 = max(self.selection_start, self.selection_end)
                i0 = int(s0 / canvas_width * len(self.audio))
                i1 = int(s1 / canvas_width * len(self.audio))
                self.segment = self.audio[i0:i1]

        self.canvas = tk.Canvas(
            self.uiroot, bg="white", width=canvas_width, height=canvas_height
        )

        y = self.audio
        n = len(y)
        y = y / max(y) * canvas_height * 0.3 + canvas_height / 2

        x = np.linspace(0, canvas_width, n)

        coords = np.zeros(n * 2)
        coords[::2] = x
        coords[1::2] = y

        self.soundtrack = self.canvas.create_line(*coords)

        self.canvas.bind("<Button-1>", mouse_down)
        self.canvas.bind("<B1-Motion>", mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", mouse_up)

        self.canvas.place(x=10, y=80)

    def start(self):
        self.uiroot.mainloop()

    def shutdown(self):
        self.uiroot.destroy()
        self.uiroot.quit()

    def open_audio(self, file=None):

        if file is None:
            self.file = fileopenbox()
        else:
            self.file = file

        print("selected audio: ", self.file)

        with sf.SoundFile(self.file) as f:
            print("Format: ", f.format)
            print("Sample rate: ", f.samplerate)
            print("Channels: ", f.channels)
            self.samplerate = f.samplerate
            data = f.read()

            # covert to simpleaudio format
            self.audio = (data * 32767 / max(abs(data))).astype(np.int16)

        self.update_canvas()

    def toggle_audio(self):
        print("toggle playing audio: ", self.file)

        if self.player and self.player.is_playing():
            self.player.stop()
        else:
            if self.segment is None:
                self.player = sa.play_buffer(self.audio, 1, 2, self.samplerate)
            else:
                self.player = sa.play_buffer(self.segment, 1, 2, self.samplerate)

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