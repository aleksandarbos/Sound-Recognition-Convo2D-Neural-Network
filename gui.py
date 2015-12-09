from Tkinter import *
import matplotlib.font_manager as font_manager
import plot

from plot import plot_audio
from recorder import Recorder


class Gui:

    def __init__(self, root):
        self.root = root
        self.create_window(root)
        self.create_record(root)
        self.create_presentation(root)
        self.create_result(root)

    def create_window(self, root):
        root.title("Soft Sound")
        root.geometry("350x450")
        root.resizable(height=FALSE, width=FALSE)

    def create_record(self, root):
        frame_record = Frame(root)
        frame_record.pack(side=TOP, fill=BOTH, pady=(0,5))
        frame_record1 = Frame(frame_record)
        frame_record1.pack(side=TOP, fill=BOTH, pady=(0,10))
        frame_record2 = Frame(frame_record)
        frame_record2.pack(side=BOTTOM, fill=NONE)

        l_caption = Label(frame_record1, text="Record sound:")
        l_caption.pack(side=LEFT);
        b_help = Button(frame_record1, text="info", width=3, height=1)
        b_help.pack(side=RIGHT)

        global b_start
        global l_time
        b_start = Button(frame_record2, text='Record', width=12, height=2, command=Controls.main_button_click)
        b_start.pack(pady=10, padx=15, side=LEFT)
        l_time = Label(frame_record2, height=1, width=5, state='disabled', bg='white', text='00:00', foreground='black')
        l_time.pack(pady=10, padx=(10,0), side=LEFT)
        l_status = Label(frame_record2, text="...recording", foreground='red')
        l_status.pack(pady=10, padx=(5,10), side=LEFT)
        b_reset = Button(frame_record2, text='Reset', padx=2, command=Controls.reset_button_click)
        b_reset.pack(pady=10, padx=20, side=LEFT)

    def create_presentation(self, root):
        frame_presentation = Frame(root, bd=4, bg='red')
        frame_presentation.pack(side=TOP, fill=BOTH)
        frame_presentation2 = Frame(frame_presentation, pady=135)
        frame_presentation2.pack(side=TOP, fill=BOTH)

        l_resulttt = Label(frame_presentation2, text="(here be picture)")
        l_resulttt.pack()

    def create_result(self, root):
        frame_result = Frame(root)
        frame_result.pack(side=BOTTOM, fill=BOTH)

        l_result = Label(frame_result, text="Recognized sound:")
        l_result.pack(pady=10, padx=5, side=LEFT)
        t_result = Text(frame_result, height=1, width=20, state='disabled')
        t_result.pack(pady=10, padx=5, side=LEFT)

        b_details = Button(frame_result, text='Details')
        b_details.pack(pady=10, padx=5, side=LEFT)

    @staticmethod
    def change_time(time):
        l_time["text"] = time

class Controls:
    @staticmethod
    def main_button_click():
        if (b_start["text"] == "Record"):
            b_start["text"] = "Analyze"
            Recorder.start_recording()
        else:
            b_start["text"] = "Record"
            plot_audio("test.wav", "fft")

    @staticmethod
    def reset_button_click():
        b_start["text"] = "Record"
        Gui.change_time("00:00")