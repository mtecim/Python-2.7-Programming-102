from Tkinter import *
import ttk
import tkFileDialog
import anydbm
import pickle
import xlrd
from recommendations import *
import csv


master_dict={}

user_dict={}

class Rating:
    def __init__(self,cafe,score):
         self.cafe = cafe
         self.score = score
    def get_full(self):
        return (self.cafe,self.score)

class User:
    def __init__(self,username,rate_dict):
        self.username=username
        self.rate_dict=rate_dict

class myGUI(Frame):
    def __init__(self, main_window):
        self.main_window = main_window
        Frame.__init__(self, self.main_window)

        self.selected_dict={}
        self.user_object = User("user",self.selected_dict)
        self.initUI(self.main_window)

    def initUI(self,main_window):
        self.label1 = Label(main_window, bg="spring green", fg="red",padx=10,pady=10, text="CAFE RECOMMENDER", font="Helvatica 18")
        self.label1.pack(fill=BOTH,)

        self.frame2 = Frame(main_window, borderwidth=2,bg="spring green" ,relief=SOLID)
        self.frame2.pack(fill=BOTH, anchor=NW,)
        self.frame3 = Frame(main_window, borderwidth=2, bg="spring green" ,relief=SOLID)
        self.frame3.pack(fill=BOTH, anchor=NW, expand=1)
        self.frame4 = Frame(self.frame3, borderwidth=2, bg="spring green",relief=SOLID)
        self.frame4.pack(side=LEFT, fill=BOTH,)

        self.frame5A = Frame(self.frame3, borderwidth=2, bg="Grey", relief=SOLID)
        self.frame5A.pack(side=LEFT, fill=BOTH, expand=1)

        self.frame5 = Frame(self.frame5A, borderwidth=2, bg="spring green",relief=SOLID)
        self.frame5.pack(side=LEFT, fill=BOTH, expand=1)

        self.frame7 = Frame(self.frame5A, borderwidth=2, bg="spring green",relief=SOLID)
        self.frame7a = Frame(self.frame7, borderwidth=2, bg="spring green")
        self.frame7b = Frame(self.frame7, borderwidth=2,bg="spring green" )
        self.frame7a.pack(side=LEFT,expand=1,fill=Y)
        self.frame7b.pack( side=LEFT,expand=1,fill=Y)

        self.frame6 = Frame(self.frame3, borderwidth=2, bg="spring green", relief=SOLID)
        self.frame6.pack(side=LEFT, fill=BOTH,)

        self.frame8 = Frame(self.frame3, borderwidth=2, bg="spring green",relief=SOLID)
        self.frame9 = Frame(self.frame3, borderwidth=2, bg="spring green", relief=SOLID)
        #########################
        # frame2

        self.uploadcafe=Button(self.frame2, text="Upload Cafe Data",bg="red",fg="white",padx=10,pady=10,command=self.uploadcafedata)
        self.uploadcafe.pack(side=LEFT,padx=100,pady=10)
        self.uploadratings = Button(self.frame2, text="Upload Ratings",padx=10,pady=10, bg="red", fg="white",command=self.uploadratingsdata)
        self.uploadratings.pack(side=RIGHT,padx=100,pady=10)
        ########################
        # frame4

        self.rating = Button(self.frame4, height=8, width=3,wraplength=1,  text="RATING", bg="red", fg="white", padx=5, pady=5,command=self.rating)
        self.rating.pack(padx=10,pady=20)
        self.recommended = Button(self.frame4, height=8, width=3,wraplength=1, text="RECOMMEND", padx=5, pady=5, bg="red", fg="white", command=self.recommend)
        self.recommended.pack(padx=10,pady=20)

        #########################
        # frame5

        l1=Label(self.frame5,text="Choose Cafe",font="Helvatica 18",bg="spring green")
        l1.pack(padx=10, pady=10)

        self.box_value = StringVar()
        self.box = ttk.Combobox(self.frame5,width=30, textvariable=self.box_value,)
        self.box.pack(padx=10, pady=10,)

        l2 = Label(self.frame5, text="Choose Rating",font="Helvatica 18", bg="spring green" )
        l2.pack(padx=10, pady=10)

        self.scale= Scale(self.frame5, from_=1, to=10, orient=HORIZONTAL,bg="spring green",length=200)
        self.scale.pack(padx=10, pady=10)

        add = Button(self.frame5, text= "     ADD      ", padx=10, pady=10, bg="red",fg="white",command=self.add )
        add.pack(padx=10, pady=10)

###########################################################################################

        self.Tree_widget = ttk.Treeview(self.frame6,height=15)
        self.Tree_widget["columns"] = ("n", "s")
        self.Tree_widget.column("n", width=150)
        self.Tree_widget.column("s", width=100)
        self.Tree_widget.heading("n", text="Cafe")
        self.Tree_widget.heading("s", text="Rating")
        self.Tree_widget['show'] = 'headings'

        self.Tree_widget.pack(side=LEFT, anchor=CENTER,padx=10, pady=5)

        remove = Button(self.frame6, text= " REMOVE ", padx=10, pady=10, bg="red",fg="white",command=self.remove)
        remove.pack(side=LEFT,padx=10)

        ##################################################
        # #frame7
        self.label7a=Label(self.frame7a,text= "Settings:",bg="spring green", font=("Helvatica", "18","underline"))
        self.label7b=Label(self.frame7a,text= "Number of Recomemdation:",bg="spring green", font="Helvatica 10 bold ")
        self.label7c = Label(self.frame7a, text="Similarity Metrics:",padx=10,bg="spring green", font="Helvatica 10 bold ")
        self.button7=Button(self.frame7b,height=2,bg="red", fg="white",width=10 ,text="Recommend Similar User",wraplength=100,command=self.recommenduser)
        self.button72=Button(self.frame7b,height=2,bg="red", fg="white", width=10,text="Recommend  Cafe",wraplength=80,command=self.recommendcafe)
        self.e1=Entry(self.frame7a,width=7,)
        self.labelx=Label(self.frame7a,bg="spring green")
        self.labelxx = Label(self.frame7b, bg="spring green")

        self.sim_var = StringVar()
        self.sim_var.set("Euclidean")
        self.cb1=Checkbutton(self.frame7a,text= "Euclidean",bg="spring green",variable=self.sim_var,onvalue="Euclidean")
        self.cb2 = Checkbutton(self.frame7a,text= "Pearson" ,bg="spring green",variable=self.sim_var,onvalue="Pearson")
        self.cb3 = Checkbutton(self.frame7a, text= "Jaccard",bg="spring green",variable=self.sim_var,onvalue="Jaccard")

        self.label7a.pack(padx=10,pady=10)
        self.label7b.pack()
        self.e1.pack(pady=15)
        self.labelx.pack(pady=20)

        self.label7c.pack(pady=15)
        self.cb1.pack()
        self.cb2.pack()
        self.cb3.pack()

        self.labelxx.pack(pady=50)
        self.button7.pack(pady=10)
        self.button72.pack()
        ###################################################
        # frame 8
        self.label8 = Label(self.frame8, text="Similiar Cafes", bg="spring green",
                             font="Helvatica 10 bold ")
        self.label8.pack(fill=BOTH)

        self.cafTree_widget = ttk.Treeview(self.frame8, height=15)
        self.cafTree_widget["columns"] = ("n", "s")
        self.cafTree_widget.column("n", width=175)
        self.cafTree_widget.column("s", width=125)
        self.cafTree_widget.heading("n", text="Recommended Caffe")
        self.cafTree_widget.heading("s", text="Score")
        self.cafTree_widget['show'] = 'headings'
        ###################################################
        # frame 9
        self.label8 = Label(self.frame9, text="Similiar User", bg="spring green",
                            font="Helvatica 10 bold ")
        self.userTree_widget = ttk.Treeview(self.frame9, height=5)
        self.userTree_widget["columns"] = ("n", "s")
        self.userTree_widget.column("n", width=175)
        self.userTree_widget.column("s", width=125)
        self.userTree_widget.heading("n", text="User")
        self.userTree_widget.heading("s", text="Score")
        self.userTree_widget['show'] = 'headings'

        self.button9 = Button(self.frame9, text="Get User Rating",command=self.sipuser)


        self.uTree_widget = ttk.Treeview(self.frame9, height=5)
        self.uTree_widget["columns"] = ("n", "s")
        self.uTree_widget.column("n", width=175)
        self.uTree_widget.column("s", width=125)
        self.uTree_widget.heading("n", text="Cafe")
        self.uTree_widget.heading("s", text="Rating")
        self.uTree_widget['show'] = 'headings'



    def uploadcafedata(self):

        dosya = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                      filetypes=(("Excel files", ".xlsx"), ("all files", "*.*")))
        cafedata = xlrd.open_workbook(dosya, "rb").sheet_by_index(0)
        cafe_list= []
        for column in range(1):
            for row in range(37):
                c=cafedata.cell(row+1,column).value
                cafe_list.append(c)
        self.box['values']=cafe_list


    def uploadratingsdata(self):

        file =tkFileDialog.askopenfilename(title="Select file",
                                                  filetypes=(("Data-base files", "*.db"), ("all files", "*")))


        ratingdata = anydbm.open(file, "c")
        for i,j in ratingdata.items():
            master_dict[i] = pickle.loads(j)


    def rating(self):
        self.frame5.pack(side=LEFT, fill=BOTH, expand=1)
        self.frame6.pack(side=LEFT, fill=BOTH, )
        self.frame7.pack_forget()
        self.frame8.pack_forget() or self.frame9.pack_forget()

    def recommend(self):
        self.frame7.pack(side=LEFT, fill=BOTH, expand=1)
        self.frame5.pack_forget()
        self.frame6.pack_forget()
        self.frame8.pack(side=LEFT, fill=BOTH, expand=1)
        tempt_dict={}
        tempt_dict.setdefault(self.user_object.username,self.user_object.rate_dict) #when we turn on recommendation part our master dict updated
        master_dict.update(tempt_dict)


    def add(self):

        cafe = self.box.get()
        score = self.scale.get()
        rate_object = Rating(cafe,score)
        self.selected_dict[cafe] = score
        self.Tree_widget.insert("","end",text="Line 1",values=rate_object.get_full())


    def remove(self):

        selected_item = self.Tree_widget.selection()[0]
        item_to_delete = self.Tree_widget.item(selected_item)["values"][0]

        self.Tree_widget.delete(selected_item)
        self.Tree_widget.update()
        del self.selected_dict[item_to_delete]

    def recommenduser(self):
        self.frame8.pack_forget()
        self.frame9.pack(side=LEFT,fill=BOTH,expand=1)
        self.userTree_widget.delete(
            *self.userTree_widget.get_children())  # https://stackoverflow.com/questions/22812134/how-to-clear-an-entire-treeview-with-tkinter
        self.label8.pack(side=TOP, anchor=N, pady=5)
        self.userTree_widget.pack(side=TOP, anchor=N, pady=5)
        self.button9.pack(side=TOP, anchor=N, pady=5)

        score=[]
        person=[]

        self.similarUsers = topMatches(master_dict, "user", n=int(self.e1.get()), similarity=sim_pearson)
        recom=self.similarUsers
        number_to_show = int(self.e1.get())
        splitted_recom = recom[0:number_to_show]
        print splitted_recom
        print recom

        for i in range(len(splitted_recom)):
            score.append(splitted_recom[i][0])
            person.append(splitted_recom[i][1])
        self.Score = score
        self.recperson = person

        for i in range(len(self.Score)):
            self.userTree_widget.insert("", "end", text="Line 1", values=(self.recperson[i],
                                                                         self.Score[i]))



    def recommendcafe(self):
        self.frame8.pack(side=LEFT, fill=BOTH, expand=1)
        self.frame9.pack_forget()

        self.cafTree_widget.delete(*self.cafTree_widget.get_children()) #https://stackoverflow.com/questions/22812134/how-to-clear-an-entire-treeview-with-tkinter
        self.cafTree_widget.pack(side=TOP, anchor=N, pady=5)

        Score = []
        Cafee = []

        itemsim = calculateSimilarItems(master_dict)
        recom = getRecommendedItems(master_dict, itemsim, self.user_object.username)
        number_to_show = int(self.e1.get())
        splitted_recom = recom[0:number_to_show]
        print splitted_recom


        for i in range(len(splitted_recom)):
            Score.append(splitted_recom[i][0])
            Cafee.append(splitted_recom[i][1])
        self.cafScore = Score
        self.recCafee = Cafee

        for i in range(len(self.cafScore)):
            self.cafTree_widget.insert("", "end", text="Line 1", values=(self.recCafee[i],
                                                                         self.cafScore[i]))

    def sipuser(self):

        self.label10 = Label(self.frame9, text="User's Rating", bg="spring green",
                             )
        self.label10.pack()
        self.uTree_widget.delete(*self.uTree_widget.get_children())
        self.uTree_widget.pack(side=TOP, anchor=N, pady=5)

        selected_item = self.userTree_widget.selection()[0]
        item_to_show = self.userTree_widget.item(selected_item)["values"][0]

        self.a=master_dict[item_to_show].keys()
        self.b=master_dict[item_to_show].values()

        for i in range(len(self.a)):
            self.uTree_widget.insert("", "end", text="Line 1", values=(self.a[i],
                                                                         self.b[i]))


def main():
    root = Tk()
    root.geometry("800x500")
    app = myGUI(root)
    root.mainloop()
main()
