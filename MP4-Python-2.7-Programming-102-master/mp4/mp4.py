from Tkinter import *
import ttk
import tkFileDialog
import anydbm
import pickle
import xlrd

from bs4 import BeautifulSoup
import urllib2
# from mysearchengine import *
import re
import shelve

main_dict={}
pokemonlist=[]

class myGUI(Frame):
    def __init__(self, main_window):
        self.main_window = main_window
        Frame.__init__(self, self.main_window)
        self.initUI(self.main_window)

    def initUI(self, main_window):
        # 2 main frame
        self.frame1=Frame(main_window)
        self.frame1.pack(side=LEFT,fill=BOTH)
        # frame2 for sowing data
        self.frame2=Frame(main_window,bg="red")

        # header
        self.label1 = Label(self.frame1, bg="red", fg="white", text="POKEDEX",relief="solid",
                                font="Helvatica 15 bold")
        self.label1.pack(fill=X)

##################################################################################################################

        self.frame3=Frame(self.frame1,bg="red",borderwidth=2,  relief=SOLID)
        self.frame3.pack(fill=X,expand=1)

        self.b1=Button(self.frame3,text="Fetch Pokemon Data",width=10,wraplength=85,bg="yellow",command=lambda s:s.get())
        self.b1.pack(side=LEFT,padx=10,pady=10)

        self.progress_bar = Canvas(self.frame3, bg='grey', width=150, height=15, borderwidth=1, relief='sunken')
        self.progress_bar.pack(side=LEFT,padx=10,pady=10)

##################################################################################################################
        self.frame4 = Frame(self.frame1,bg="red", borderwidth=2,  relief=SOLID)
        self.frame4.pack(fill=X)

        self.label2=Label(self.frame4,bg="red",text="Searhing&Filtering")
        self.label2.pack()

        self.e1=Entry(self.frame4,width=40,relief=SUNKEN)
        self.e1.pack()

        self.label3=Label(self.frame4,bg="red",text="Filter by tyoe:")
        self.label3.pack(anchor=W,padx=10)

        self.box_value=StringVar

        self.combobox=ttk.Combobox(self.frame4,width=25, textvariable=self.box_value)
        self.combobox.pack(side=LEFT,padx=12,pady=10)

        self.b2 = Button(self.frame4, text="SEARCH",bg="yellow", command=self.search)
        self.b2.pack(side=LEFT,padx=10,pady=10)

##################################################################################################################
        self.frame5=Frame(self.frame1,bg="red", borderwidth=2,  relief=SOLID)
        self.frame5.pack()

        self.label4=Label(self.frame5,bg="red",text="Total:  Result")
        self.label4.pack()

        self.listbox1 = Listbox(self.frame5, borderwidth=1, width=30, relief="solid")
        self.listbox1.pack(side=LEFT,padx=12,pady=10)

        self.b3 = Button(self.frame5, text="Get Pokemon Data",bg="yellow", command=self.getdata)
        self.b3.pack(side=LEFT,padx=10,pady=10)


    def load(self):
        tempt_dict={}
        dosya1 = open("all_pokemon.txt", "r")
        for line in dosya1:
            main_dict.setdefault(line,tempt_dict)
        # print main_dict

        for key in main_dict.keys():
            global attributes
            response = urllib2.urlopen("https://www.pokemon.com/us/pokedex/"+key.lower())
            html_doc = response.read()
            soup = BeautifulSoup(html_doc, "html.parser")


            pics=soup.find_all("img",{"class":"active"})
            names=soup.find_all("div",{"class":"pokedex-pokemon-pagination-title"})
            a=names.text
            attributes=soup.find_all("span",{"class":"attribute-value"})

            print a
            # print names[0].string
            print "*"*500
            # print attributes.text
            # print tept_dict
            # type=soup.find_all("a",{"href":""})
            # weakness=soup.find_all("a",{"href":""})
            #
            # print names
            # print pics
            # print attributes


    def search(self):
        self.listbox1.delete(0,END)
        try:
            for key in main_dict.keys():
                if self.e1.get().lower() in key.lower():
                    self.listbox1.insert(END, key)
                else:
                    print "there is not match"

        except len(main_dict)==0:
            print "you didnot upload data"



    def getdata(self):
        #about pics
        # import urllib
        # image_element = driver.find_element_by_id('chartImg')
        # src = image_element.get_attribute("src")
        # if src:
        #     urllib.urlretrieve(str(src), "test.png")


        label=Label(self.frame2,text="           "*10)
        label.pack(fill=X)
        self.frame2.pack(side=LEFT,fill=BOTH,expand=1)


def main():
    root = Tk()
    root.geometry()
    app = myGUI(root)
    root.mainloop()
main()