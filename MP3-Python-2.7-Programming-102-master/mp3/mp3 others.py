#https://stackoverflow.com/questions/16790328/open-multiple-filenames-in-tkinter-and-add-the-filesnames-to-a-list=> for multiple file dialog
#https://stackoverflow.com/questions/42942534/how-to-change-the-color-of-a-tkinter-label-programmatically => for changing label color to green
#https://stackoverflow.com/questions/17125842/changing-the-text-on-a-label for changing label text
#https://stackoverflow.com/a/45669789 => for displaying image on canvas
#https://stackoverflow.com/questions/7727804/tkinter-using-scrollbars-on-a-canvas => for scrollbar
#https://pythonspot.com/tk-message-box/ => for dialog box
#https://blogs.harvard.edu/rprasad/2014/06/16/reading-excel-with-python-xlrd/ => for reading excel file
#https://stackoverflow.com/questions/13842088/set-value-for-particular-cell-in-pandas-dataframe-using-index => for setting specific cell of df
#https://stackoverflow.com/questions/16957226/encode-python-list-to-utf-8 => for encode u'string' to string
#https://stackoverflow.com/questions/13295735/how-can-i-replace-all-the-nan-values-with-zeros-in-a-column-of-a-pandas-datafra => for filling df null cell with 0
#https://stackoverflow.com/questions/19585280/convert-a-row-in-pandas-into-list => for convert df row to list
#https://stackoverflow.com/questions/17241004/how-do-i-get-the-data-frame-index-as-an-array => for getting label of clusters from df indexes
#https://xlrd.readthedocs.io/en/latest/api.html => for reading excel file
#https://stackoverflow.com/questions/14050824/add-sum-of-values-of-two-lists-into-new-list for collecting individually two list elements to one / for summing two list elements to one list ??
#https://stackoverflow.com/questions/14538885/how-to-get-the-index-with-the-key-in-python-dictionary

from math import sqrt
import random
import PIL.Image as pilImage
import PIL.ImageTk as imagetk
import tkMessageBox
from Tkinter import *
import tkFileDialog
import xlrd
from os import path
from xlrd import open_workbook
from math import sqrt
import PIL.ImageDraw as pilImageDraw


class clusters():

    def pearson(self, v1, v2):
        # Simple sums
        sum1 = sum(v1)
        sum2 = sum(v2)

        # Sums of the squares
        sum1Sq = sum([pow(v, 2) for v in v1])
        sum2Sq = sum([pow(v, 2) for v in v2])

        # Sum of the products
        pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

        # Calculate r (Pearson score)
        num = pSum-(sum1*sum2/len(v1))
        den = sqrt((sum1Sq-pow(sum1, 2)/len(v1))*(sum2Sq-pow(sum2, 2)/len(v1)))
        if den == 0:
            return 0

        return 1.0-num/den

    class bicluster:
        def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
            self.left = left
            self.right = right
            self.vec = vec
            self.id = id
            self.distance = distance

    def hcluster(self, rows):
        distances = {}
        currentclustid = -1

        #clust = [bicluster(restaurantDict[restaurant], id=i) for i,restaurant in enumerate(restaurantDict)]
        # Clusters are initially just the rows
        clust = [self.bicluster(rows[key], id=i)
                 for i, key in enumerate(rows.keys())]

        while len(clust) > 1:
            lowestpair = (0, 1)
            closest = self.pearson(clust[0].vec, clust[1].vec)

            # loop through every pair looking for the smallest distance
            for i in range(len(clust)):
                for j in range(i+1, len(clust)):
                    # distances is the cache of distance calculations
                    if (clust[i].id, clust[j].id) not in distances:
                        distances[(clust[i].id, clust[j].id)] = self.pearson(
                            clust[i].vec, clust[j].vec)

                    d = distances[(clust[i].id, clust[j].id)]

                    if d < closest:
                        closest = d
                        lowestpair = (i, j)

            # calculate the average of the two clusters
            mergevec = [(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]
                                                           ].vec[i])/2.0 for i in range(len(clust[0].vec))]

            # create the new cluster
            newcluster = self.bicluster(
                mergevec, left=clust[lowestpair[0]], right=clust[lowestpair[1]], distance=closest, id=currentclustid)

            # cluster ids that weren't in the original set are negative
            currentclustid -= 1
            del clust[lowestpair[1]]
            del clust[lowestpair[0]]

            clust.append(newcluster)

        return clust[0]

    def printclust(self, clust, labels=None, n=0):
        # indent to make a hierarchy layout
        for i in range(n):
            print ' ',
        if clust.id < 0:
            # negative id means that this is branch
            print '-'
        else:
            # positive id means that this is an endpoint
            if labels == None:
                print clust.id
            else:
                print labels[clust.id]

        # now print the right and left branches
        if clust.left != None:
            self.printclust(clust.left, labels=labels, n=n+1)
        if clust.right != None:
            self.printclust(clust.right, labels=labels, n=n+1)

    def getheight(self, clust):
        # Is this an endpoint? Then the height is just 1
        if clust.left == None and clust.right == None:
            return 1

        # Otherwise the height is the same of the heights of
        # each branch
        return self.getheight(clust.left)+self.getheight(clust.right)

    def getdepth(self, clust):
        # The distance of an endpoint is 0.0
        if clust.left == None and clust.right == None:
            return 0

        # The distance of a branch is the greater of its two sides
        # plus its own distance
        return max(self.getdepth(clust.left), self.getdepth(clust.right))+clust.distance

    def drawdendrogram(self, clust, labels, jpeg='clusters.jpg'):
        # height and width
        h = self.getheight(clust)*20
        w = 1200
        depth = self.getdepth(clust)

        # width is fixed, so scale distances accordingly
        scaling = float(w-150)/depth

        # Create a new image with a white background
        img = pilImage.new('RGB', (w, h), (255, 255, 255))
        # img.thumbnail(size=(1000,1000))
        draw = pilImageDraw.Draw(img)

        draw.line((0, h/2, 10, h/2), fill=(255, 0, 0))

        # Draw the first node
        self.drawnode(draw, clust, 10, (h/2), scaling, labels)

        return img
        try:
            img.save(jpeg, 'JPEG')
        except:
            img.save(jpeg, 'JPEG')

    def drawnode(self, draw, clust, x, y, scaling, labels):
        if clust.id < 0:
            h1 = self.getheight(clust.left)*20
            h2 = self.getheight(clust.right)*20
            top = y-(h1+h2)/2
            bottom = y+(h1+h2)/2
            # Line length
            ll = clust.distance*scaling
            # Vertical line from this cluster to children
            draw.line((x, top+h1/2, x, bottom-h2/2), fill=(255, 0, 0))

            # Horizontal line to left item
            draw.line((x, top+h1/2, x+ll, top+h1/2), fill=(255, 0, 0))

            # Horizontal line to right item
            draw.line((x, bottom-h2/2, x+ll, bottom-h2/2), fill=(255, 0, 0))

            # Call the function to draw the left and right nodes
            self.drawnode(draw, clust.left, x+ll, top+h1/2, scaling, labels)
            self.drawnode(draw, clust.right, x+ll,
                          bottom-h2/2, scaling, labels)
        else:
            # If this is an endpoint, draw the item label
            draw.text((x+5, y-7), labels[clust.id], (0, 0, 0))

    def rotatematrix(self, data):
        newdata = []
        for i in range(len(data[0])):
            newrow = [data[j][i] for j in range(len(data))]
            newdata.append(newrow)
        return newdata

    def kcluster(self, rows, distance=pearson, k=4):
        # Determine the minimum and maximum values for each point
        ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows]))
                  for i in range(len(rows[0]))]

        # Create k randomly placed centroids
        clusters = [[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0]
                     for i in range(len(rows[0]))] for j in range(k)]

        lastmatches = None
        for t in range(100):
            print 'Iteration %d' % t
            bestmatches = [[] for i in range(k)]

            # Find which centroid is the closest for each row
            for j in range(len(rows)):
                row = rows[j]
                bestmatch = 0
                for i in range(k):
                    d = distance(clusters[i], row)
                    if d < distance(clusters[bestmatch], row):
                        bestmatch = i
                bestmatches[bestmatch].append(j)

            # If the results are the same as last time, this is complete
            if bestmatches == lastmatches:
                break
            lastmatches = bestmatches

            # Move the centroids to the average of their members
            for i in range(k):
                avgs = [0.0]*len(rows[0])
                if len(bestmatches[i]) > 0:
                    for rowid in bestmatches[i]:
                        for m in range(len(rows[rowid])):
                            avgs[m] += rows[rowid][m]
                    for j in range(len(avgs)):
                        avgs[j] /= len(bestmatches[i])
                    clusters[i] = avgs

        return bestmatches

    def tanimoto(self, v1, v2):
        c1, c2, shr = 0, 0, 0

        for i in range(len(v1)):
            if v1[i] != 0:
                c1 += 1  # in v1
            if v2[i] != 0:
                c2 += 1  # in v2
            if v1[i] != 0 and v2[i] != 0:
                shr += 1  # in both

        return 1.0-(float(shr)/(c1+c2-shr))

    def scaledown(self, data, distance=pearson, rate=0.01):
        n = len(data)

        # The real distances between every pair of items
        realdist = [[distance(data[i], data[j]) for j in range(n)]
                    for i in range(0, n)]

        # Randomly initialize the starting points of the locations in 2D
        loc = [[random.random(), random.random()] for i in range(n)]
        fakedist = [[0.0 for j in range(n)] for i in range(n)]

        lasterror = None
        for m in range(0, 1000):
            # Find projected distances
            for i in range(n):
                for j in range(n):
                    fakedist[i][j] = sqrt(sum([pow(loc[i][x]-loc[j][x], 2)
                                               for x in range(len(loc[i]))]))

            # Move points
            grad = [[0.0, 0.0] for i in range(n)]

            totalerror = 0
            for k in range(n):
                for j in range(n):
                    if j == k:
                        continue
                    # The error is percent difference between the distances
                    errorterm = (fakedist[j][k]-realdist[j][k])/realdist[j][k]

                    # Each point needs to be moved away from or towards the other
                    # point in proportion to how much error it has
                    grad[k][0] += ((loc[k][0]-loc[j][0]) /
                                   fakedist[j][k])*errorterm
                    grad[k][1] += ((loc[k][1]-loc[j][1]) /
                                   fakedist[j][k])*errorterm

                    # Keep track of the total error
                    totalerror += abs(errorterm)
            print totalerror

            # If the answer got worse by moving the points, we are done
            if lasterror and lasterror < totalerror:
                break
            lasterror = totalerror

            # Move each of the points by the learning rate times the gradient
            for k in range(n):
                loc[k][0] -= rate*grad[k][0]
                loc[k][1] -= rate*grad[k][1]

        return loc

    def draw2d(self, data, labels, jpeg='mds2d.jpg'):
        img = pilImage.new('RGB', (2000, 2000), (255, 255, 255))
        draw = pilImageDraw.Draw(img)
        for i in range(len(data)):
            x = (data[i][0]+0.5)*1000
            y = (data[i][1]+0.5)*1000
            draw.text((x, y), labels[i], (0, 0, 0))
        img.save(jpeg, 'JPEG')




class data():

    excelSheets = []
    clusterObj = clusters()

    def readAllFiles(self, excelPaths):
        self.excelSheets

        del self.excelSheets[:]

        for excelPath in excelPaths:
            self.excelSheets.append(open_workbook(excelPath).sheets()[0])
        # all excel files were readed and assigned to a list which named self.excelSheets

    def clusterBasedOnFood(self):

        distinctMealCodes = []  # all restaurants distinct meal codes
        vector_dict = {}  # vector dict {key = restaurant name : value = bool type vector}, vector index is 1 whether restaurant include meal or 0

        for sheet in self.excelSheets:
            number_of_rows = sheet.nrows

            mealCodes = []  # current restaurant menu

            for row in range(2, number_of_rows):
                mealCodes.append((sheet.cell(row, 0).value).encode("utf-8"))

            # meal codes added to all restaurant meal codes
            distinctMealCodes.extend(mealCodes)

        # dublicate records were deleted
        distinctMealCodes = list(set(distinctMealCodes))

        for sheet in self.excelSheets:

            # default vector for vector_dict varriable (all records is 0 by default)
            currentRestDefVector = [0] * len(distinctMealCodes)
            number_of_rows = sheet.nrows

            restaurantName = (sheet.cell(0, 1).value).encode("utf-8")

            countryCode = (sheet.cell(0, 2).value).encode("utf-8")
            # restaurantName string appended with countryCode
            restaurantName = restaurantName + " (" + countryCode + ")"

            curentRestaurantMenu = []

            for row in range(2, number_of_rows):
                # current restaurant menu were assigned to "curentRestaurantMenu" list
                curentRestaurantMenu.append(
                    (sheet.cell(row, 0).value).encode("utf-8"))

            curentRestaurantMenu = list(set(curentRestaurantMenu))

            for mealCode in curentRestaurantMenu:
                if mealCode in distinctMealCodes:
                    currentRestDefVector[distinctMealCodes.index(mealCode)] = 1
                    # default vector cell set to 1 if restaurant contain a mealcode

            vector_dict[restaurantName] = currentRestDefVector

        cluster = self.clusterObj.hcluster(vector_dict)
        # vector dict keys are restaurant names as labels of result image
        image = self.clusterObj.drawdendrogram(cluster, vector_dict.keys())

        return image

    def clusterFoodBasedOnRestaurant(self):

        distinctMealCodes = []
        # key = restaurant name : value = vector that contains menu(meal codes)
        restaurantMenus_dict = {}
        vector_dict = {}  # key = meal code : value = vector, vector cell is 1 if restaurant include meal or 0 if not

        for sheet in self.excelSheets:
            number_of_rows = sheet.nrows

            mealCodes = []

            restName = (sheet.cell(0, 1).value).encode("utf-8")

            for row in range(2, number_of_rows):
                mealCodes.append((sheet.cell(row, 0).value).encode("utf-8"))

            mealCodes = list(set(mealCodes))
            restaurantMenus_dict[restName] = mealCodes

            distinctMealCodes.extend(mealCodes)

        for mealCode in distinctMealCodes:
            currentVector = [0] * len(restaurantMenus_dict)

            for rest in restaurantMenus_dict:
                currentRestMenu = restaurantMenus_dict[rest]

                if mealCode in currentRestMenu:
                    currentVector[restaurantMenus_dict.keys().index(rest)] = 1
                else:
                    currentVector[restaurantMenus_dict.keys().index(rest)] = 0
                    # current vector cell set to 1 if mealcode in current restaurant
            vector_dict[mealCode] = currentVector

        cluster = self.clusterObj.hcluster(vector_dict)
        image = self.clusterObj.drawdendrogram(cluster, vector_dict.keys())

        return image

    def clusterRestBasedOnRating(self):

        distinctMealCodes = []
        mealRating_dict = {}  # key = meal code : value = meal rating
        vector_dict = {}  # key = restaurant name : key = vector that contains meal rating

        for sheet in self.excelSheets:
            number_of_rows = sheet.nrows

            mealCodes = []

            for row in range(2, number_of_rows):
                mealCodes.append((sheet.cell(row, 0).value).encode("utf-8"))

            distinctMealCodes.extend(mealCodes)
            distinctMealCodes = list(set(distinctMealCodes))

        for sheet in self.excelSheets:
            currentFoodMealVector = [0] * len(distinctMealCodes)
            number_of_rows = sheet.nrows

            for row in range(2, number_of_rows):
                meal = (sheet.cell(row, 0).value).encode("utf-8")

                rating = (sheet.cell(row, 2).value)
                # current restaurant ratings were assigned to mealRating_dict
                mealRating_dict[meal] = rating

            restName = (sheet.cell(0, 1).value).encode("utf-8")
            restRating = sheet.cell(0, 3).value

            # restaurantName string appended with restaurant rating
            restName = restName + " (" + str(restRating) + ")"

            for mealCode in distinctMealCodes:
                if mealCode in mealRating_dict.keys():
                    currentFoodMealVector[distinctMealCodes.index(
                        mealCode)] = mealRating_dict[mealCode]
                    # currentFood vector dict cells were set with meal rating

            vector_dict[restName] = currentFoodMealVector
            # current meals and ratings dict was cleared for prevent combining next restaurants menu and rating
            mealRating_dict.clear()

        cluster = self.clusterObj.hcluster(vector_dict)
        image = self.clusterObj.drawdendrogram(cluster, vector_dict.keys())

        return image

class Application(Frame):

    dataUploaded = False

    dataObj = data()

    def loadResturantsClick(self):
        excelFilePaths = tkFileDialog.askopenfilenames(
            initialdir=path.dirname(path.abspath(__file__)), title="Select file")

        self.dataObj.readAllFiles(excelFilePaths)
        # excel file paths were selected with a dialog box and sent to related function

        self.dataUploadText_lbl.config(bg="green")
        self.dataUploadText_lbl.config(text='Data uploaded')
        self.dataUploaded = True
        # the label that indicate "data upload" were set

    def restBasedFoodCluster_click(self):

        if self.dataUploaded:
                    # whether data was uploaded was checked ?

                    # if data is uploaded

            root.geometry("900x600")
            # main frame was expanded

            image = self.dataObj.clusterBasedOnFood()
            # clustering result image was assigned to image variable

            self.image = imagetk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.image, anchor=NW)
            # result image was placed in canvas

            self.hbar.pack(side=BOTTOM, fill=X)
            self.vbar.pack(side=RIGHT, fill=Y)
            self.canvas.pack()
            # canvas and scroll bars were placed

            self.canvas_frm.update()
            self.update()
        else:
            tkMessageBox.showerror("Error", "Load Data Before Clustering")
            # if data is not uploaded then show message box

        print "restBasedFoodCluster_click"

    def foodBasedOnRest_click(self):
        if self.dataUploaded:
            root.geometry("900x600")

            temp = self.dataObj.clusterFoodBasedOnRestaurant()
            self.image = imagetk.PhotoImage(temp)

            self.canvas.create_image(50, 10, image=self.image, anchor=NW)

            self.hbar.pack(side=BOTTOM, fill=X)
            self.vbar.pack(side=RIGHT, fill=Y)
            self.canvas.pack()

            self.update()
        else:
            tkMessageBox.showerror("Error", "Load Data Before Clustering")

        print "restBasedRatingCluster_click"

    def restBasedOnRating_click(self):
        if self.dataUploaded:
            root.geometry("900x600")

            temp = self.dataObj.clusterRestBasedOnRating()
            self.image = imagetk.PhotoImage(temp)

            self.canvas.create_image(50, 10, image=self.image, anchor=NW)

            self.hbar.pack(side=BOTTOM, fill=X)
            self.vbar.pack(side=RIGHT, fill=Y)
            self.canvas.pack()

            self.update()
        else:
            tkMessageBox.showerror("Error", "Load Data Before Clustering")

        print "restBasedOnRating_click"

    def createWidgets(self):

        self.blue_frm = Frame(root, width=900, height=17, bg="blue")
        self.mainTitle_lbl = Label(self.blue_frm, width=900, text="Restaurants Clustering Tool",
                                   justify="center", font='Helvetica 17 bold', bg="blue", fg="white")
        self.mainTitle_lbl.pack(padx=150)

        self.blue_frm.pack()
        # main text was placed with a frame

        # -----------------------------------------------------------
        self.uploadButton_frm = Frame(root, width=900, height=90)

        self.dataUploadText_lbl = Label(self.uploadButton_frm, text="Data not uploaded",
                                        justify="center", font='Helvetica 12', bg="red", fg="black")
        self.dataUploadText_lbl.pack(side=RIGHT, padx=10)

        self.loadRestData_btn = Button(self.uploadButton_frm, text="Load Resturants Data",
                                       command=self.loadResturantsClick, width=25, height=3, fg="black", font="Helvetica 10 bold")
        self.loadRestData_btn.pack(side=LEFT)

        self.uploadButton_frm.pack()
        # upload data butttons were and label placed with a frame

        # ----------------------------------------------------

        self.clusterButtons_frm = Frame(root, width=900, height=90)

        self.restBasedFoodCluster_btn = Button(self.clusterButtons_frm, text="Cluster Resturant based on Food",
                                               command=self.restBasedFoodCluster_click, width=35, height=3, fg="black", font="Helvetica 10 bold")
        self.restBasedFoodCluster_btn.pack(side=LEFT)

        self.restBasedOnRating_btn = Button(self.clusterButtons_frm, text="Cluster Resturant based on Rating",
                                            command=self.restBasedOnRating_click, width=35, height=3, fg="black", font="Helvetica 10 bold")
        self.restBasedOnRating_btn.pack(side=LEFT)

        self.foodBasedOnRest_btn = Button(self.clusterButtons_frm, text="Cluster Food based on Resturants",
                                          command=self.foodBasedOnRest_click, width=35, height=3, fg="black", font="Helvetica 10 bold")
        self.foodBasedOnRest_btn.pack(side=LEFT)

        self.clusterButtons_frm.pack(pady=10)
        # clustering buttons were placed with a frame

        # --------------------------------------------------------

        self.canvas_frm = Frame(root, width=900, height=90)
        self.canvas = Canvas(self.canvas_frm, width=700,
                             height=250, scrollregion=(50, 0, 1215, 2520))

        self.hbar = Scrollbar(self.canvas_frm, orient=HORIZONTAL)
        self.hbar.config(command=self.canvas.xview)

        self.vbar = Scrollbar(self.canvas_frm, orient=VERTICAL)
        self.vbar.config(command=self.canvas.yview)

        self.canvas.config(xscrollcommand=self.hbar.set,
                           yscrollcommand=self.vbar.set)

        self.canvas_frm.pack(pady=2)
        # the canvas that contain result image was placed with a frame

        # --------------------------------------------------------------

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
root.geometry("900x180")
app = Application(master=root)
app.mainloop()
