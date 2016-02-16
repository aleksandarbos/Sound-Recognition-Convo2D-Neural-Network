#######################
# File: tkoutput.py
# Author: A.J. Gauld
# Date: September 2001
#
from Tkinter import *
import sys
import threading

class Display(Frame):
    ''' Demonstrate python interpreter output in Tkinter Text widget

type python expression in the entry, hit DoIt and see the results
in the text pane.'''

    def __init__(self,parent=0):
       Frame.__init__(self,parent)

       self.scrollbar = Scrollbar(parent)
       self.scrollbar.pack(side=RIGHT, fill=Y)

       self.output = Text(self, wrap=WORD, yscrollcommand=self.scrollbar.set)
       self.output.pack()
       sys.stdout = self
       self.pack()

       self.scrollbar.config(command=self.output.yview)



    def write(self, txt):
        self.output.insert(END,str(txt))

if __name__ == '__main__':
    Display().mainloop()
