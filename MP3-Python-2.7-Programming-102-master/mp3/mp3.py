from Tkinter import *
import ttk
import tkFileDialog
import anydbm
import pickle
import xlrd
import PIL
import clusters
import csv
from PIL import Image, ImageTk

totalresfood = {}
food_list = []
totalresrating ={}



class Cluster:
    def __init__(self, resname, food, data):
        self.resname=resname
        self.food=food
        self.data=data



class myGUI(Frame):
    def __init__(self, main_window):
        self.main_window = main_window
        Frame.__init__(self, self.main_window)
        self.initUI(self.main_window)
    def initUI(self,main_window):
        #header

        self.label1 = Label(main_window, bg="blue", fg="white", text="Resturants Clustering Tool", font="Helvatica 15 bold")
        self.label1.pack(fill=BOTH)

        ########################################################################################################################
        #in first frame i have load data button and label, in second frame i have cluster butons
        self.frame1=Frame()
        self.frame1.pack()
        self.frame2 = Frame()
        self.frame2.pack()
        self.uploadresturants = Button(self.frame1,width=30 ,text="Load Resturants Data",padx=10, pady=10,
                                 command=self.loaddata)
        self.uploadresturants.pack(side=LEFT,padx=5,pady=0)

        self.label2 = Label(self.frame1, bg="red", fg="black", text="Data not uploaded")
        self.label2.pack(side=LEFT,anchor=E)

        self.clusterbasedonfood = Button(self.frame2,width=30, text="Cluster Resturants based on Food", padx=10, pady=10,
                                    command=self.clusbasedonfood)
        self.clusterbasedonfood.pack(side=LEFT, padx=2, pady=2)

        self.clusterbasedonrating = Button(self.frame2,width=30, text="Cluster Resturants based on Rating", padx=10, pady=10,
                                         command=self.clusbasedonrating)
        self.clusterbasedonrating.pack(side=LEFT)

        self.clusterfood = Button(self.frame2,width=30, text="Cluster Food based on  Resturants ", padx=10, pady=10,
                                         command=self.clusfood)

        self.clusterfood.pack(side=LEFT, padx=2, pady=2)

        #########################################################################################################################################################

        #in 3. frame it is a main frame for output of clustering button. ALL 3 FRAME ENTER INTO THIS FRAME
        #for scrollbar using i check the link https://stackoverflow.com/questions/7727804/tkinter-using-scrollbars-on-a-canvas?rq=1
        self.frame3=Frame()
        self.frame3.pack(fill=BOTH, expand=1)

        self.frame7=Frame(self.frame3)

        #########################################################################################################################################################
        self.frame4 = Frame(self.frame3,)

        self.canvas1 = Canvas(self.frame4, bg="red", width=660, height=250, scrollregion=(0, 0, 1200, 1100))
        self.h1 = Scrollbar(self.frame4, orient=HORIZONTAL)
        self.h1.pack(side=BOTTOM, fill=X)
        self.h1.config(command=self.canvas1.xview)
        self.v1 = Scrollbar(self.frame4, orient=VERTICAL)
        self.v1.pack(side=RIGHT, fill=Y)
        self.v1.config(command=self.canvas1.yview)
        self.canvas1.config(xscrollcommand=self.h1.set, yscrollcommand=self.v1.set)
        self.canvas1.pack(side=LEFT, expand=True, fill=BOTH)

        ##################################################################### #####################################################################
        self.frame5=Frame(self.frame3,)
        # create a canvas and place in frame
        self.canvas2 = Canvas(self.frame5, bg="red", width=660, height=250,scrollregion=(0,0,1200,1100))
        self.h2=Scrollbar(self.frame5,orient=HORIZONTAL)
        self.h2.pack(side=BOTTOM,fill=X)
        self.h2.config(command=self.canvas2.xview)
        self.v2=Scrollbar(self.frame5,orient=VERTICAL)
        self.v2.pack(side=RIGHT, fill=Y)
        self.v2.config(command=self.canvas2.yview)
        self.canvas2.config(xscrollcommand=self.h2.set, yscrollcommand=self.v2.set)
        self.canvas2.pack(side=LEFT, expand=True, fill=BOTH)

        ##################################################################### #####################################################################
        self.frame6=Frame(self.frame3,)

        # create a canvas and place in frame
        self.canvas3 = Canvas(self.frame6, bg="red", width=660, height=250, scrollregion=(0, 0, 1200, 3100))
        self.h3 = Scrollbar(self.frame6, orient=HORIZONTAL)
        self.h3.pack(side=BOTTOM, fill=X)
        self.h3.config(command=self.canvas3.xview)
        self.v3 = Scrollbar(self.frame6, orient=VERTICAL)
        self.v3.pack(side=RIGHT, fill=Y)
        self.v3.config(command=self.canvas3.yview)
        self.canvas3.config(xscrollcommand=self.h3.set, yscrollcommand=self.v3.set)
        self.canvas3.pack(side=LEFT, expand=True, fill=BOTH)

        ##################################################################### ######################################################################

        self.lab1=Label(self.frame7,text="Cutting Point:",padx=30)
        self.e1=Entry(self.frame7,width=5)
        self.run=Button(self.frame7,text="Run Analysis",width=25,padx=10,)
        self.lab2 = Label(self.frame7, text="Clusters")
        self.list=Listbox(self.frame7,width=40)

        self.lab1.pack(side=LEFT)
        self.e1.pack(side=LEFT,padx=10)
        self.run.pack(side=LEFT)
        self.lab2.pack(side=TOP)
        self.list.pack(side=TOP,pady=10)

    def loaddata(self):
        #for each exel in data folder i read all of them
        dosyalar = tkFileDialog.askopenfilename(initialdir="/", title="Select file",multiple=1,
                                             filetypes=(("Excel files", ".xlsx"), ("all files", "*.*")))
        class dosyalarclass:
            def __init__(self,x):
                self.dosyamm=x
            def dosyamiac(self):
                return self.dosyamm
        x=dosyalarclass(dosyalar)
        self.sonuc=x.dosyamiac()
##########################################################################################################################################################

        for dosya in self.sonuc:
            temp_food_list = []

            data = xlrd.open_workbook(dosya, "rb").sheet_by_index(0)
            for dosya in xrange(data.nrows):
                temp_food_list.append(data.cell_value(dosya, 1).encode("utf-8"))
                #for food in excel i append them into temproroy list
                #i create a dic for key is resturant name and values are food
                totalresfood[temp_food_list[0]] = temp_food_list[2:]
        print totalresfood
        #check is there any data uploaded if there is any data config label
        if len(self.sonuc)==130:
            self.label2.config(  bg="green", fg="white", text="Data is uploaded :)", font="13")
            print len(self.sonuc)
        else:
            print "you didnot upload all docs it must be upload. it must be 130 excel files."
        #create a text file which is input for clustering
        basedonfoodtxt = open("ResFood.txt", "w")
        #create a total food list for existing all food in data
        for foods in totalresfood.values():
            for food in foods:
                if food not in food_list:
                    food_list.append(food)

        basedonfoodtxt.write("foodsekrem\t")#its for 0,0 in matrix
        for food in food_list:
            basedonfoodtxt.write("\t%s" %food)
        basedonfoodtxt.write('\n')#write all food in total food list into text file

        for key,values in totalresfood.items():
            basedonfoodtxt.write(key)#write all resturants
            basedonfoodtxt.write("\t")

            for food in food_list:
                if food not in values:
                    basedonfoodtxt.write("0\t")

                else:
                   basedonfoodtxt.write(("1\t"))
            basedonfoodtxt.write('\n')

        basedonfoodtxt.close()
        #the reason why i crate this ResFood.txt in Load data is this txt important for both 1. and 3. cluster. If i create this in first cluster part i couldnt use it before cluster 1 run.
##################################################################################################################################################################

    def clusbasedonfood(self):
        self.frame4.pack_forget()
        self.frame5.pack_forget()
        self.frame6.pack_forget()
        self.frame7.pack_forget()

        a,b,c = clusters.readfile('ResFood.txt')
        c1 = Cluster(a,b,c)
        clust = clusters.hcluster(c1.data)
        clusters.drawdendrogram(clust, c1.resname, jpeg="RFC.jpg")#draw jpeg of hierarciahl clusters
        self.image1 = Image.open("RFC.jpg")
         #after drawing jpg give it as a image 1 to the canvas and pack it in frame4

        self.photo = ImageTk.PhotoImage(self.image1)
        self.canvas1.create_image(0, 0, image=self.photo, anchor=NW)
        self.frame4.pack()
        self.frame7.pack(side=BOTTOM, fill=BOTH, expand=1)

#########################################################################################################################################################

    def clusbasedonrating(self):
        self.frame5.pack_forget()
        self.frame4.pack_forget()
        self.frame6.pack_forget()
        self.frame7.pack_forget()


        basedonratingtxt = open("ResRating.txt", "w")
        # like other one i create a text file and i read data and classify them
        for dosya in self.sonuc:
            temp_f_list = []
            temp_rating_list = []
            data = xlrd.open_workbook(dosya, "rb").sheet_by_index(0)
            for dosya in xrange(data.nrows):
                temp_f_list.append(data.cell_value(dosya, 1).encode("utf-8"))#takes food in excel
                temp_rating_list.append(data.cell_value(dosya, 2))#takes health rates in excel
                totalresrating[temp_f_list[0]] = temp_f_list[2:],temp_rating_list[2:]#create a dict has a value existing food list and rating list

        temp_dict = {}

        for i in totalresrating.keys():
            temp_dict.setdefault(i,{})
            foods, ratings = totalresrating[i]
            for j in range(len(foods)):
                temp_dict[i][foods[j]]=ratings[j]

        basedonratingtxt.write("Food\t")

        for food in food_list:
            basedonratingtxt.write("\t%s" % food)

        basedonratingtxt.write("\n")
        for j in totalresrating.keys():
            basedonratingtxt.write(j + "\t")
            for i in food_list:
                if i in temp_dict[j]:
                    basedonratingtxt.write(str(temp_dict[j][i]) + "\t")
                else:
                    basedonratingtxt.write("0" + "\t")
            basedonratingtxt.write("\n")
        basedonratingtxt.close()

        e, f, g = clusters.readfile('ResRating.txt')
        c2 = Cluster(e, f, g)
        clust = clusters.hcluster(c2.data)
        clusters.drawdendrogram(clust, c2.resname, jpeg="RRC.jpg")
        #clustering txt file

        #give file to canvas
        self.image2 = Image.open("RRC.jpg")
        self.photo = ImageTk.PhotoImage(self.image2)
        self.canvas2.create_image(0, 0, image=self.photo, anchor=NW)
        self.frame5.pack()
        self.frame7.pack(side=BOTTOM, fill=BOTH, expand=1)

#########################################################################################################################################################
    def clusfood(self):
        self.frame4.pack_forget()
        self.frame5.pack_forget()
        self.frame6.pack_forget()
        self.frame7.pack_forget()

        #cluster food is just a rotated form of first cluster.We rotate matrix and cluster it.
        resname,food,data = clusters.readfile("ResFood.txt")
        rdata = clusters.rotatematrix(data)
        newclust = clusters.hcluster(rdata)
        clusters.drawdendrogram(newclust,food, jpeg="FC.jpg")

        self.image3 = Image.open("FC.jpg")
        self.photo = ImageTk.PhotoImage(self.image3)
        self.canvas3.create_image(0, 0, image=self.photo, anchor=NW)

        self.frame6.pack()
        self.frame7.pack(side=BOTTOM, fill=BOTH, expand=1)


def main():
    root = Tk()
    root.geometry()
    app = myGUI(root)
    root.mainloop()
main()




