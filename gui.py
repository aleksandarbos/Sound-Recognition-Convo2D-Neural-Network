import tkFileDialog
import threading
import winsound, sys

from Tkinter import *
from recorder import Recorder
from plot import  Plot


class Gui:

    timer = None

    def __init__(self, root):
        self.l_selected_file_name_var = StringVar()      # variable for label dynamic text
        self.l_timer_var = StringVar()

        self.selected_file_name = ""                     # variable for storaging global selected file name
        self.counter = 0                                 # clock counter

        self.b_waveform = []                             # declaring plot buttons
        self.b_fft = []
        self.l_status = []
        self.full_file_path = []

        self.radioIntVar = []                            # 2D or more dimensions plot

        menu_bar = Menu(root)
        file_menu = Menu(menu_bar, tearoff=0)

        self.root = root
        self.create_window(root)
        self.create_record(root)
        #self.create_presentation(root)             izbacen preview iz gui-a
        self.create_result(root)
        self.create_menu_bar(root, menu_bar, file_menu)

        self.root.config(menu=menu_bar)
        self.root.mainloop()


    def handleRadioSel(self):
        if(self.radioIntVar.get() == 1):
            self.b_spectrogram['state'] = 'active'
        elif(self.radioIntVar.get() == 2):
            self.b_spectrogram['state'] = 'disabled'

    def open_audio_file(self):
        sys.stdout.write("Searching for file...")
        options = {}
        options['filetypes'] = [('WAV audio files', '.wav')]
        self.full_file_path = tkFileDialog.askopenfilename(**options)
        splitted_path = self.full_file_path.split('/')
        file_name = splitted_path[len(splitted_path)-1]
        self.selected_file_name = file_name         #global var, selected file_name
        self.l_selected_file_name_var.set("[Selected file name]: " + self.selected_file_name)

        self.b_fft['state'] = 'active'         # enable plot buttons
        self.b_waveform['state'] = 'active'
        self.b_spectrogram['state'] = 'active'

        print "\n[Selected file name:] " + file_name

    def create_menu_bar(self, root, menu_bar, file_menu):
        file_menu.add_command(label = "Open audio file", command = self.open_audio_file)
        menu_bar.add_cascade(label="File", menu=file_menu)


    def create_window(self, root):
        root.title("Sound Recognition - Soft Computing")
        root.geometry("550x200")
        root.resizable(height=FALSE, width=FALSE)

    def create_record(self, root):
        frame_record = Frame(root)
        frame_record.pack(side=TOP, fill=BOTH, pady=(0,5))
        frame_record1 = Frame(frame_record)
        frame_record1.pack(side=TOP, fill=BOTH, pady=(0,10))
        frame_record2 = Frame(frame_record)                    #12 between 1 and 2
        frame_record2.pack(side=TOP, fill=BOTH, pady=(0,10))
        frame_record3 = Frame(frame_record)
        frame_record3.pack(side=BOTTOM, fill=NONE)

        l_caption = Label(frame_record1, text="Record sound:")
        l_caption.pack(side=LEFT)
        b_help = Button(frame_record1, text="info", width=3, height=1)
        b_help.pack(side=RIGHT)

        self.l_selected_file_name_var = StringVar()
        self.l_selected_file_name_var.set("[Selected file name:] none")

        l_selected_file_name = Label(frame_record2, textvariable = self.l_selected_file_name_var, width = 30, height = 1, anchor = 'w')
        l_selected_file_name.pack(side = LEFT)

        self.b_waveform = Button(frame_record2, text = "WaveForm", width = 8, height = 1, command = lambda : Plot.plot_audio(self.full_file_path, "raw", self.radioIntVar))
        self.b_waveform.pack(side = RIGHT)
        self.b_waveform['state'] = 'disabled'

        self.b_fft = Button(frame_record2, text = "FFT", width = 8, height = 1, command = lambda : Plot.plot_audio(self.full_file_path, "fft", self.radioIntVar))
        self.b_fft.pack(side = RIGHT, padx = 3)
        self.b_fft['state'] = 'disabled'

        self.b_spectrogram = Button(frame_record2, text = "Spectrogram", width = 10, height = 1, command = lambda : Plot.plot_audio(self.full_file_path, "spectrogram", self.radioIntVar))
        self.b_spectrogram.pack(side = RIGHT, padx = 3)
        self.b_spectrogram['state'] = 'disabled'

        self.radioIntVar = IntVar()
        R1 = Radiobutton(frame_record2, text="2D", variable=self.radioIntVar, value=1, command= lambda: self.handleRadioSel())
        R1.pack( side = RIGHT)
        self.radioIntVar.set(1)     # init 2D as default

        R2 = Radiobutton(frame_record2, text="3D", variable=self.radioIntVar, value=2, command= lambda: self.handleRadioSel())
        R2.pack( side = RIGHT)


        global b_start
        global l_time
        b_start = Button(frame_record3, text='Record', width=12, height=2, command=lambda: self.main_button_click())
        b_start.pack(pady=10, padx=15, side=LEFT)

        self.l_timer_var.set('00:00')
        l_time = Label(frame_record3, height=1, width=5, state='disabled', bg='white', textvariable=self.l_timer_var, foreground='black')
        l_time.pack(pady=10, padx=(10,0), side=LEFT)
        l_status = Label(frame_record3, text="...recording", foreground='red')
        l_status.pack(pady=10, padx=(5,10), side=LEFT)
        b_reset = Button(frame_record3, text='Reset', padx=2, command=self.reset_button_click())
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
        frame_result.pack(fill=BOTH)

        l_result = Label(frame_result, text="Recognized sound:")
        l_result.pack(pady=10, padx=5, side=LEFT)
        t_result = Text(frame_result, height=1, width=20, state='disabled')
        t_result.pack(pady=10, padx=5, side=LEFT)

        b_details = Button(frame_result, text='Details')
        b_details.pack(pady=10, padx=5, side=RIGHT)

    def tick_timer(self):
        timer = threading.Timer(1, self.tick_timer)
        timer.start()
        self.counter += 1
        if self.counter > 9:
            self.l_timer_var.set('00:' + str(self.counter))
        else:

            self.l_timer_var.set('00:0' + str(self.counter))

        if self.counter > 3:                                    # 3 secs for duration of recording
            timer.cancel()
            self.play_beep()
            self.counter = 0
            self.l_timer_var.set('00:00')
            return

        print "tick..." + str(self.counter)

    def main_button_click(self):
        self.play_beep()
        self.tick_timer()
        Recorder.start_recording()
        self.full_file_path = "test.wav"
        self.l_selected_file_name_var.set("[Selected file name]: " + "test.wav")
        self.b_spectrogram['state'] = 'active'

    def reset_button_click(self):
        b_start["text"] = "Record"

    def play_beep(self):
        winsound.PlaySound("beep.wav", winsound.SND_ALIAS)
