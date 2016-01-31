import tkFileDialog
import threading

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


        menu_bar = Menu(root)
        file_menu = Menu(menu_bar, tearoff=0)

        self.root = root
        self.create_window(root)
        self.create_record(root)
        self.create_presentation(root)
        self.create_result(root)
        self.create_menu_bar(root, menu_bar, file_menu)

        self.root.config(menu=menu_bar)
        self.root.mainloop()



    def open_audio_file(self):
        sys.stdout.write("Searching for file...")
        options = {}
        options['filetypes'] = [('WAV audio files', '.wav')]
        file_path = tkFileDialog.askopenfilename(**options)
        splitted_path = file_path.split('/')
        file_name = splitted_path[len(splitted_path)-1]
        self.selected_file_name = file_name         #global var, selected file_name
        self.l_selected_file_name_var.set("[Selected file name]: " + self.selected_file_name)

        self.b_fft['state'] = 'active'         # enable plot buttons
        self.b_waveform['state'] = 'active'

        print "\n[Selected file name:] " + file_name

    def create_menu_bar(self, root, menu_bar, file_menu):
        file_menu.add_command(label = "Open audio file", command = self.open_audio_file)
        menu_bar.add_cascade(label="File", menu=file_menu)


    def create_window(self, root):
        root.title("Soft Sound")
        root.geometry("350x450")
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

        l_selected_file_name = Label(frame_record2, textvariable = self.l_selected_file_name_var, width = 25, height = 1, anchor = 'w')
        l_selected_file_name.pack(side = LEFT)

        self.b_waveform = Button(frame_record2, text = "WaveForm", width = 8, height = 1, command = lambda : Plot.plot_audio(self.selected_file_name, "raw"))
        self.b_waveform.pack(side = RIGHT)
        self.b_waveform['state'] = 'disabled'

        self.b_fft = Button(frame_record2, text = "FFT", width = 8, height = 1, command = lambda : Plot.plot_audio(self.selected_file_name, "fft"))
        self.b_fft.pack(side = RIGHT, padx = 3)
        self.b_fft['state'] = 'disabled'

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
        frame_result.pack(side=BOTTOM, fill=BOTH)

        l_result = Label(frame_result, text="Recognized sound:")
        l_result.pack(pady=10, padx=5, side=LEFT)
        t_result = Text(frame_result, height=1, width=20, state='disabled')
        t_result.pack(pady=10, padx=5, side=LEFT)

        b_details = Button(frame_result, text='Details')
        b_details.pack(pady=10, padx=5, side=LEFT)

    def tick_timer(self):
        timer = threading.Timer(1, self.tick_timer)
        timer.start()
        self.counter += 1
        if self.counter > 9:
            self.l_timer_var.set('00:' + str(self.counter))
        else:

            self.l_timer_var.set('00:0' + str(self.counter))

        if self.counter > 5:                                    # 3 secs for duration of recording
            timer.cancel()
            self.counter = 0
            self.l_timer_var.set('00:00')
            return

        print "tick..." + str(self.counter)

    def main_button_click(self):
        self.tick_timer()
        Recorder.start_recording()


    def reset_button_click(self):
        b_start["text"] = "Record"
        #Gui.change_time("00:00")