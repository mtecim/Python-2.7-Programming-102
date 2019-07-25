
import csv

from Tkinter import *

SelectionList=[]

class Createfile:
    def __init__(self,filename,type):
        self.filename = filename
        self.type = type
    def get_full_name(self):
       self.fname = self.filename + "." + self.type
       return self.fname

class myGUI(Frame):
    def __init__(self, main_window):
        self.main_window = main_window
        Frame.__init__(self, self.main_window)
        self.initUI(self.main_window)


    def initUI(self,main_window):
        #first main frames and widgets
        self.frame1 = Frame(main_window, borderwidth=2,  relief=SOLID)
        self.frame1.pack(fill=BOTH, anchor=NW,)

        self.frame11 = Frame(self.frame1)
        self.frame1a=Frame(self.frame1)
        self.frame1b=Frame(self.frame1)
        self.frame1c=Frame(self.frame1)

        self.frame11.pack(fill=BOTH)
        self.frame1a.pack(anchor=W,)
        self.frame1b.pack(anchor=W,)
        self.frame1c.pack(anchor=W,)

        headlabel = Label(self.frame11,padx=15,pady=15, text="Sehir Cafeteria", bg="blue", fg="red")
        headlabel.pack(anchor=CENTER, fill=BOTH)

        l1=Label(self.frame1a, text="File Path:     ")
        self.e1=Entry(self.frame1a)

        l1.pack(side=LEFT)
        self.e1.pack(side=LEFT)

        l2=Label(self.frame1b,text="Choose your Diet:    ")
        l2.pack(side=LEFT)

        global var
        var = IntVar()

        R1 = Radiobutton(self.frame1b, text="1300 kcal   ", variable=var, value=1300,
                         command=self.radiobuttons)
        R1.pack(side=LEFT,anchor=W)

        R2 = Radiobutton(self.frame1b, text="1800 kcal   ", variable=var, value=1800,
                         command=self.radiobuttons)
        R2.pack(side=LEFT,anchor=W)

        R3 = Radiobutton(self.frame1b, text="2400 kcal                       ", variable=var, value=2400,
                         command=self.radiobuttons)
        R3.pack(side=LEFT,anchor=W)


        self.l3 = Label(self.frame1c)
        self.l3.pack(side=LEFT)

        countinue1= Button(self.frame1,text="Countinue",bg="red", command=self.continue1)
        countinue1.pack(side=LEFT)

###########################################################################################################################
        #second main window and its widgets
        self.frame2 = Frame(self.main_window, borderwidth=2, relief=SOLID)
        self.part2frame = Frame(self.frame2, )
        self.part2frame1 = Frame(self.frame2 )
        self.part2frame2 = Frame(self.frame2, )
        self.part2frame3 = Frame(self.frame2)
        self.part2frame4 = Frame(self.frame2)

        self.part2frame.pack(side=TOP, fill=X, )
        self.part2frame4.pack(side=BOTTOM, anchor=W)
        self.part2frame1.pack(side=LEFT, fill=BOTH, padx=10, anchor=W, expand=TRUE)
        self.part2frame2.pack(side=LEFT, anchor=W, expand=TRUE)
        self.part2frame3.pack(side=LEFT, anchor=W, fill=BOTH, padx=10, expand=TRUE)

        # up frame in second main window
        self.part2l1 = Label(self.part2frame, text="Choose Your Food")
        self.part2l1.pack(fill=X)

        self.part2l2 = Label(self.part2frame1, text="Food Menu", padx=10, pady=10)
        self.part2l2.pack()
        self.listbox1 = Listbox(self.part2frame1, borderwidth=1, relief="solid")
        self.listbox1.pack(fill=BOTH, expand=1)

        # middle frame in second main window
        self.removefood = Button(self.part2frame2, text="Remove Food", bg="red", command=self.removefood)
        self.removefood.pack(side=BOTTOM)

        self.addfood = Button(self.part2frame2, text="Add Food", bg="red", command=self.addfood)
        self.addfood.pack(side=BOTTOM)

        # left frame in second main window

        self.part2l3 = Label(self.part2frame3, text="My Food", padx=10, pady=10)
        self.part2l3.pack()

        self.listbox2 = Listbox(self.part2frame3, borderwidth=1, relief="solid")
        self.listbox2.pack(fill=BOTH, expand=1)

        # bottom frame in second main window only continuie button

        self.countinue2 = Button(self.part2frame4, text="Countinue", bg="red", command=self.continue2)
        self.countinue2.pack(side=BOTTOM, anchor=W)
#################################################################################################

        #third main window and widgets

        self.frame3 = Frame(self.main_window, borderwidth=2, relief=SOLID)
        self.frame31 = Frame(self.frame3)
        self.frame31.pack(fill=BOTH)
        self.l31 = Label(self.frame31, text="Summary and Data Saving")
        self.l31.pack()
        self.l32= Label(self.frame3)
        self.l32.pack( anchor=W)
        self.l33=Label(self.frame3,)
        self.l33.pack( anchor=W)

        self.l34=Label(self.frame3,text= "Choose File Type:   ")
        self.l34.pack(side=LEFT, anchor=W)

        self.check=IntVar()
        self.rad1 = Radiobutton(self.frame3, text="Txt File   ",variable=self.check,value=1)
        self.rad1.pack(side=LEFT)

        self.rad2 = Radiobutton(self.frame3, text="Csv File   ",variable=self.check,value=2)
        self.rad2.pack(side=LEFT)

        self.savebutton= Button(self.frame3, text="Save File  " , bg="red",command=self.writingfiles)
        self.savebutton.pack(side=LEFT)

    def radiobuttons(self):
        pass

    def middle_frame(self):
        self.frame2.pack(fill=BOTH,)

    def bottom_lastframe(self):
        self.frame3.pack(fill=BOTH, expand=TRUE)

    def continue1(self):
        selection = "Your Diet Choice is " + str(var.get()) + "  kcal"
        self.middle_frame()
        self.l3.config(text=selection)
        self.l32.config(text=selection)
        yemek_dict = {}
        dosya = open(self.e1.get(),"r")
        satirlar = dosya.readlines()
        satirlar.remove(satirlar[0])
        self.listbox1.insert(END,"Choice - Price - Calorie")
        for i in satirlar:
            liste = i.strip("\n").split(",")
            kalori = liste[0]
            yemek = liste[1]
            fiyat = liste[2]
            #printing food into listbox
            temp_str = yemek + ", " + fiyat + "TL, " + kalori + " kcal"
            self.listbox1.insert(END,temp_str)

    def continue2(self):
        self.bottom_lastframe()
        self.totalkcal = 0
        for i in SelectionList:
            liste = i.strip("\n").split(",")
            yemek = liste[0]
            fiyat = liste[1]
            kalori = liste[2]

            k=kalori.strip("\n").split(" ")
            kcal = k[1]
            print kalori
            # calculating total kalori in selection lists strings by slipliting
            # print k,kcal
            self.totalkcal+= int(kcal)
            # print totalkcal

        if self.totalkcal>var.get():
            self.l33.config(text="Your Choosen Food Menu-Amount of Calories: " + str(self.totalkcal) + " kcal above daily limit",bg="red")
        else:
            self.l33.config(text="Your Choosen Food Menu-Amount of Calories: " + str(self.totalkcal) + " kcal ",bg="green")

    def addfood(self):
        self.ustunde = self.listbox1.curselection()[0] #selecting listbox items
        self.myfood = self.listbox1.get(self.ustunde) #getting selected food as myfood
        if self.myfood =="Choice - Price - Calorie":
            print "Please select something has calorie"
        else:
            self.listbox2.insert(END, self.myfood)
            SelectionList.append(self.myfood)
            print SelectionList

    def removefood(self):
        self.ustunde = self.listbox2.curselection()[0]
        self.myfood = self.listbox2.get(self.ustunde)
        self.delete=self.listbox2.delete(self.ustunde)
        SelectionList.remove(self.myfood)
        # print SelectionList

    def writingfiles(self):
        if self.check.get()==1:

            txt_object = Createfile("My_Food_Choices", "txt")
            dosya = open(txt_object.get_full_name(), "w")
            for i in SelectionList:
                yemek = i.split(", ")[0]
                fiyat = i.split(", ")[1]
                kalori = i.split(", ")[2]
                strr_yemek = yemek.encode("utf-8")
                #decode and encode using for clarify problems for writing Turkish caracters It change their types to str.
                satir = "You ordered ".decode("utf-8") + strr_yemek.decode("utf-8") + " price: ".decode(
                 "utf-8") + fiyat.decode("utf-8") + " calories: ".decode("utf-8") + kalori.decode("utf-8")
                dosya.write(satir.encode("utf-8"))
                dosya.write("\n")

            dosya.write("\n")
            dosya.write("-" * 20)
            dosya.write("\nTotal calories :  " + str(self.totalkcal))

        elif self.check.get()==2:

            csv_object = Createfile("My_Food_Choices", "csv")
            dosya2 = open(csv_object.get_full_name(), "w")
            dosya2.write("You ordered,Price,Calories,Total Calories\n")

            for i in SelectionList:
                yemek = i.split(", ")[0]
                fiyat = i.split(", ")[1]
                kalori = i.split(", ")[2]
                strr_yemek = yemek.encode("utf-8")

                satir = strr_yemek.decode("utf-8") + ",".decode("utf-8") + fiyat.decode("utf-8") + ",".decode(
                    "utf-8") + kalori.decode("utf-8") + ",".decode("utf-8") + str(self.totalkcal).decode("utf-8")
                dosya2.write(satir.encode("utf-8"))
                dosya2.write("\n")

def main():
    root = Tk()
    root.geometry()
    app = myGUI(root)
    root.mainloop()
main()
# FoodDB.csv for controlling program