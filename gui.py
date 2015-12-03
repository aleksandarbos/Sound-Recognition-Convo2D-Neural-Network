from Tkinter import *
import tkMessageBox

def create_window(root):
    root.title("Soft Sound")
    root.geometry("350x100")
    #root.geometry("350x450")
    root.resizable(height=FALSE, width=FALSE)

def create_record(root):
    frame_record = Frame(root)
    frame_record.pack(side=TOP, fill=BOTH, pady=(0,5))
    frame_record1 = Frame(frame_record)
    frame_record1.pack(side=TOP, fill=BOTH, pady=(0,10))
    frame_record2 = Frame(frame_record)
    frame_record2.pack(side=BOTTOM, fill=NONE)

    l_caption = Label(frame_record1, text="Record sound:")
    l_caption.pack(side=LEFT);
    b_help = Button(frame_record1, text="info", padx=0.5, pady=0.5)
    b_help.pack(side=RIGHT)

    b_start = Button(frame_record2, text='Start / Stop', padx=15, pady=8, command=buttonclick)
    b_start.pack(pady=10, padx=20, side=LEFT)
    l_time = Text(frame_record2, height=1, width=5, state='disabled')
    l_time.pack(pady=10, padx=(10,0), side=LEFT)
    l_status = Label(frame_record2, text="...recording", foreground='red')
    l_status.pack(pady=10, padx=(5,10), side=LEFT)
    b_reset = Button(frame_record2, text='Reset', padx=2)
    b_reset.pack(pady=10, padx=20, side=LEFT)

def buttonclick():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

def create_presentation(root):
    frame_presentation = Frame(root, bd=4, bg='red')
    frame_presentation.pack(side=TOP, fill=BOTH)
    frame_presentation2 = Frame(frame_presentation, pady=140)
    frame_presentation2.pack(side=TOP, fill=BOTH)

    l_resulttt = Label(frame_presentation2, text="(here be picture)")
    l_resulttt.pack()

def create_result(root):
    frame_result = Frame(root)
    frame_result.pack(side=BOTTOM, fill=BOTH)

    l_result = Label(frame_result, text="Recognized sound:")
    l_result.pack(pady=10, padx=5, side=LEFT)
    t_result = Text(frame_result, height=1, width=20, state='disabled')
    t_result.pack(pady=10, padx=5, side=LEFT)

    b_details = Button(frame_result, text='Details')
    b_details.pack(pady=10, padx=5, side=LEFT)

root = Tk()
create_window(root)
create_record(root)
create_presentation(root)
create_result(root)
root.mainloop()