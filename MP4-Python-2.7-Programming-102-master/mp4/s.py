from Tkinter import *

class myGUI(Frame):
    def __init__(self, main_window):
        self.main_window = main_window
        Frame.__init__(self, self.main_window)
        self.initUI(self.main_window)


    def initUI(self, main_window):


      self.s=StringVar()
      self.b1 = Button(main_window, text="Fetch and Train", command=    lambda :self.s.set("siktir"))
      self.b1.pack(side=LEFT, padx=5, pady=5, anchor=N)

      self.label2 = Label(main_window, textvariable=self.s   , bg="white")
      self.label2.pack(side=LEFT)
      self.b2 = Button(main_window, text="Fetch and Train", command= self.printt)
      self.b2.pack(side=LEFT, padx=5, pady=5)

    def printt(self):
        print self.s.get()


def main():
    root = Tk()
    root.geometry()
    app = myGUI(root)
    root.title()
    root.mainloop()
main()

