from Tkinter import *
import ttk
from bs4 import BeautifulSoup
import requests
import pickle
import time
from io import BytesIO
from PIL import Image, ImageTk
from resizeimage import resizeimage

class MainWindow(Frame):

    def __init__(self):
        Frame.__init__(self)

        self.master.title("POKODEX")
        #self.master.minsize(400, 100)
        self.grid(sticky=E+W+N+S)
        self.pbar_det = ttk.Progressbar(orient="horizontal", length=300, mode="determinate", maximum=151)
        self.pbar_det.grid()
        self.valCombo = ('All Types','Bug','Dragon','Electric','Fairy','Fighting','Fire','Flying', 'Grass','Ghost','Ground','Ice','Normal','Psychic','Poison','Rock','Steel','Water')
        self.varCombo = StringVar(self)
        self.varCombo.set( 'All Types' )
        self.filtre=Label(text="Filter by type").grid(row=6,column=0,sticky="w",padx=2, pady=10)
        self.combobox=ttk.Combobox(values=self.valCombo,textvariable=self.varCombo)
        self.combobox.grid(row=7,column=0,sticky="w",padx=2, pady=3)
        self.arama=Button(text="Search",command=lambda:self.Search()).grid(row=7,column=1,sticky="e",padx=2, pady=3)
        self.Poke_cekme=Button(text='Fetch Pokemon Data', command=lambda:self.vericekme()).grid(row=2, column=0, sticky="w",padx=2, pady=3)
        self.AD=Label(text="POKPDEX").grid(row=0,column=0,sticky="we",columnspan=5,padx=2, pady=10)
        self.pomenonisim=Label(text="Searching & Filtering").grid(row=4,column=0,sticky="we",padx=2, pady=10)
        self.pokemonismi=ttk.Entry(width=5)
        self.pokemonismi.grid(row=5,column=0,sticky="we",columnspan=2,padx=2, pady=3)
        self.toblamsonuc=Label(text="Total").grid(row=9,column=0,sticky="we",columnspan=5,padx=2, pady=10)
        self.pokemonisimleri=Listbox(width=25,height=10)
        self.pokemonisimleri.grid(row=10,column=0,sticky="we",padx=2, pady=10)
        self.pokemonbutonu=Button(text="Get Pokemon Data",command=lambda:self.Pokemon_veri()).grid(row=10,column=2,sticky="we",padx=2, pady=4)
        self.bosluk1=Label(bg='black',height=1).grid(row=1,column=0,columnspan=5,sticky="ew")
        self.bosluk2=Label(bg='black',height=1).grid(row=3,column=0,columnspan=5,sticky="ew")
        self.bosluk3=Label(bg='black',height=1).grid(row=8,column=0,columnspan=5,sticky="ew")
    def vericekme(self):
        self.pokemonlar=['Bulbasaur','Ivysaur','Venusaur','Charmander','Charmeleon','Charizard','Squirtle','Wartortle','Blastoise','Caterpie','Metapod','Butterfree','Weedle','Kakuna','Beedrill','Pidgey','Pidgeotto','Pidgeot','Rattata','Raticate','Spearow','Fearow','Ekans','Arbok','Pikachu','Raichu','Sandshrew','Sandslash','Nidoran-female','Nidorina','Nidoqueen','Nidoran-male','Nidorino','Nidoking','Clefairy','Clefable','Vulpix','Ninetales','Jigglypuff','Wigglytuff','Zubat','Golbat','Oddish','Gloom','Vileplume','Paras','Parasect','Venonat','Venomoth','Diglett','Dugtrio','Meowth','Persian','Psyduck','Golduck','Mankey','Primeape','Growlithe','Arcanine','Poliwag','Poliwhirl','Poliwrath','Abra','Kadabra','Alakazam','Machop','Machoke','Machamp','Bellsprout','Weepinbell','Victreebel','Tentacool','Tentacruel','Geodude','Graveler','Golem','Ponyta','Rapidash','Slowpoke','Slowbro','Magnemite','Magneton','Farfetchd','Doduo','Dodrio','Seel','Dewgong','Grimer','Muk','Shellder','Cloyster','Gastly','Haunter','Gengar','Onix','Drowzee','Hypno','Krabby','Kingler','Voltorb','Electrode','Exeggcute','Exeggutor','Cubone','Marowak','Hitmonlee','Hitmonchan','Lickitung','Koffing','Weezing','Rhyhorn','Rhydon','Chansey','Tangela','Kangaskhan','Horsea','Seadra','Goldeen','Seaking','Staryu','Starmie','Mr-Mime','Scyther','Jynx','Electabuzz','Magmar','Pinsir','Tauros','Magikarp','Gyarados','Lapras','Ditto','Eevee','Vaporeon','Jolteon','Flareon','Porygon','Omanyte','Omastar','Kabuto','Kabutops','Aerodactyl','Snorlax','Articuno','Zapdos','Moltres','Dratini','Dragonair','Dragonite','Mewtwo','Mew']
        #self.pokemonlar=['Bulbasaur','Ivysaur','Venusaur','Charmander']
        a=0
        i = 1
        pokeozellikleri=dict()
        self.Bug=list()
        self.Dragon=list()
        self.Electric=list()
        self.Fairy=list()
        self.Fighting=list()
        self.Fire=list()
        self.Flying=list()
        self.Grass=list()
        self.Ghost=list()
        self.Ground=list()
        self.Ice=list()
        self.Normal=list()
        self.Psychic=list()
        self.Poison=list()
        self.Rock=list()
        self.Steel=list()
        self.Water=list()
        for pokemon in self.pokemonlar:
    
            url = 'https://www.pokemon.com/us/pokedex/'+pokemon
    
            
            a=a+1
            print(pokemon,a)
            istek = requests.get(url)
            html = istek.content
            soup = BeautifulSoup(html, 'html.parser')
            
            
           

            
            ad = soup.find_all ('div',attrs={'class':'pokedex-pokemon-pagination-title'})
            
            pokeno = soup.find_all('span',attrs={'class':'pokemon-number'})
            
            zayiflik= soup.find_all('div',attrs={'class':'dtm-weaknesses'})[0].findChildren('span')
            
            resimurl = soup.find('img', attrs={'class': 'active'})
            
            ozellikler=soup.find_all('span',attrs={'class':'attribute-value'})
            
            tip= soup.find_all('div',attrs={'class':'dtm-type'})[0].findChildren('li')

            print resimurl
            print "*"*500

            print resimurl[0].text


            if(len(zayiflik)==1):
                zayifliklar=[zayiflik[0].text]
            elif(len(zayiflik)==2):
                zayifliklar=[zayiflik[0].text,zayiflik[1].text]
            elif(len(zayiflik)==3):
                zayifliklar=[zayiflik[0].text,zayiflik[1].text,zayiflik[2].text]
            elif(len(zayiflik)==4):
                zayifliklar=[zayiflik[0].text,zayiflik[1].text,zayiflik[2].text,zayiflik[3].text]
            elif(len(zayiflik)==5):
                zayifliklar=[zayiflik[0].text,zayiflik[1].text,zayiflik[2].text,zayiflik[3].text,zayiflik[4].text]

            if (len(tip)<=2):
                
                if(str(tip[0].text).strip()=='Bug'):
                   self.Bug.append(pokemon)
                   
                elif(str(tip[0].text).strip()=='Dragon'):
                    self.Dragon.append(pokemon)
                
                elif(str(tip[0].text).strip()=='Electric'):
                    self.Electric.append(pokemon)
                    
                elif(str(tip[0].text).strip()=='Fairy'):
                    self.Fairy.append(pokemon)
                    
                elif(str(tip[0].text).strip()=='Fighting'):
                    self.Fighting.append(pokemon)                
            
                elif(str(tip[0].text).strip()=='Fire'):
                    self.Fire.append(pokemon) 
                    
                elif(str(tip[0].text).strip()=='Flying'):
                    self.Flying.append(pokemon)
                    
                elif(str(tip[0].text).strip()=="Grass"):
                    self.Grass.append(pokemon)   
                    
                elif(str(tip[0].text).strip()=="Ghost"):
                    self.Ghost.append(pokemon) 
                
                elif(str(tip[0].text).strip()=="Ground"):
                    self.Ground.append(pokemon)
                
                elif(str(tip[0].text).strip()=="Ice"):
                    self.Ice.append(pokemon)
                    
                elif(str(tip[0].text).strip()=="Normal"):
                    self.Normal.append(pokemon)
                    
                elif(str(tip[0].text).strip()=="Psychic"):
                    self.Psychic.append(pokemon)

                elif(str(tip[0].text).strip()=="Poison"):
                    self.Poison.append(pokemon)

                elif(str(tip[0].text).strip()=="Rock"):
                    self.Rock.append(pokemon)
                    
                elif(str(tip[0].text).strip()=="Steel"):
                    self.Steel.append(pokemon)
                    
                elif(str(tip[0].text).strip()=="Water"):
                    self.Water.append(pokemon)
                    
            if (len(tip)>=2):
                if(str(tip[1].text).strip()=='Bug'):
                   self.Bug.append(pokemon)
                   
                elif(str(tip[1].text).strip()=='Dragon'):
                    self.Dragon.append(pokemon)
                
                elif(str(tip[1].text).strip()=='Electric'):
                    self.Electric.append(pokemon)
                    
                elif(str(tip[1].text).strip()=='Fairy'):
                    self.Fairy.append(pokemon)
                    
                elif(str(tip[1].text).strip()=='Fighting'):
                    self.Fighting.append(pokemon)                
            
                elif(str(tip[1].text).strip()=='Fire'):
                    self.Fire.append(pokemon) 
                    
                elif(str(tip[1].text).strip()=='Flying'):
                    self.Flying.append(pokemon)
                    
                elif(str(tip[1].text).strip()=="Grass"):
                    self.Grass.append(pokemon)   
                    
                elif(str(tip[1].text).strip()=="Ghost"):
                    self.Ghost.append(pokemon) 
                
                elif(str(tip[1].text).strip()=="Ground"):
                    self.Ground.append(pokemon)
                
                elif(str(tip[1].text).strip()=="Ice"):
                    self.Ice.append(pokemon)
                    
                elif(str(tip[1].text).strip()=="Normal"):
                    self.Normal.append(pokemon)
                    
                elif(str(tip[1].text).strip()=="Psychic"):
                    self.Psychic.append(pokemon)

                elif(str(tip[1].text).strip()=="Poison"):
                    self.Poison.append(pokemon)

                elif(str(tip[1].text).strip()=="Rock"):
                    self.Rock.append(pokemon)
                    
                elif(str(tip[1].text).strip()=="Steel"):
                    self.Steel.append(pokemon)
                    
                elif(str(tip[1].text).strip()=="Water"):
                    self.Water.append(pokemon)
            pokemon=pokemon.upper()        
            pokemonlar={pokemon:{'pokeno':pokeno[2].text,'Height':ozellikler[0].text,'Weight':ozellikler[1].text,'Category':ozellikler[3].text,'Abilities':ozellikler[4].text,'ResimURL':resimurl['src'],'Weaknesses':zayifliklar}}
            pokeozellikleri.update(pokemonlar)
            
            #print(pokeozellikleri['Venusaur'])
            
            self.pbar_det.update()
            self.pbar_det["value"] = i
            i += 1
            time.sleep(0.02)
            
        pickle.dump(pokeozellikleri,open("pokemonlar.pkl","wb"))
        
    def Search(self):
        self.pokemonisimleri.delete(0,END)
        if((self.combobox).get()=='All Types'):
           a=0
           aranan=self.pokemonismi.get()
           aranan=aranan.upper()
           for i in xrange(0,len(self.pokemonlar)):
              self.pokemonlar[a]=self.pokemonlar[a].upper()
              if (((self.pokemonlar[a]).find(aranan))>=0):
                  self.pokemonisimleri.insert(a,self.pokemonlar[a])
              a=a+1
              
        elif((self.combobox).get()=='Bug'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Bug)):
               self.Bug[a]=self.Bug[a].upper()
               if (((self.Bug[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Bug[a])
               a=a+1

        elif((self.combobox).get()=='Dragon'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Dragon)):
               self.Dragon[a]=self.Dragon[a].upper()
               if (((self.Dragon[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Dragon[a])
               a=a+1
               
        elif((self.combobox).get()=='Electric'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Electric)):
               self.Electric[a]=self.Electric[a].upper()
               if (((self.Electric[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Electric[a])
               a=a+1  
               
        elif((self.combobox).get()=='Fairy'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Fairy)):
               self.Fairy[a]=self.Fairy[a].upper()
               if (((self.Fairy[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Fairy[a])
               a=a+1  

        elif((self.combobox).get()=='Fighting'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Fighting)):
               self.Fighting[a]=self.Fighting[a].upper()
               if (((self.Fighting[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Fighting[a])
               a=a+1       

        elif((self.combobox).get()=='Fire'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Fire)):
               self.Fire[a]=self.Fire[a].upper()
               if (((self.Fire[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Fire[a])
               a=a+1  

        elif((self.combobox).get()=='Flying'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Flying)):
               self.Flying[a]=self.Flying[a].upper()
               if (((self.Flying[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Flying[a])
               a=a+1  

        elif((self.combobox).get()=='Grass'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Grass)):
               self.Grass[a]=self.Grass[a].upper()
               if (((self.Grass[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Grass[a])
               a=a+1  

        elif((self.combobox).get()=='Ghost'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Ghost)):
               self.Ghost[a]=self.Ghost[a].upper()
               if (((self.Ghost[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Ghost[a])
               a=a+1  
               
        elif((self.combobox).get()=='Ground'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Ground)):
               self.Ground[a]=self.Ground[a].upper()
               if (((self.Ground[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Ground[a])
               a=a+1  
               
        elif((self.combobox).get()=='Ice'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Ice)):
               self.Ice[a]=self.Ice[a].upper()
               if (((self.Ice[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Ice[a])
               a=a+1  
               
        elif((self.combobox).get()=='Normal'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Normal)):
               self.Normal[a]=self.Normal[a].upper()
               if (((self.Normal[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Normal[a])
               a=a+1  
               
        elif((self.combobox).get()=='Psychic'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Psychic)):
               self.Psychic[a]=self.Psychic[a].upper()
               if (((self.Psychic[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Psychic[a])
               a=a+1  
               
        elif((self.combobox).get()=='Poison'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Poison)):
               self.Poison[a]=self.Poison[a].upper()
               if (((self.Poison[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Poison[a])
               a=a+1  
               
        elif((self.combobox).get()=='Rock'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Rock)):
               self.Rock[a]=self.Rock[a].upper()
               if (((self.Rock[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Rock[a])
               a=a+1  


        elif((self.combobox).get()=='Steel'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Steel)):
               self.Steel[a]=self.Steel[a].upper()
               if (((self.Steel[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Steel[a])
               a=a+1  

        elif((self.combobox).get()=='Water'):
            a=0
            aranan=self.pokemonismi.get()
            aranan=aranan.upper()
            for i in xrange(0,len(self.Water)):
               self.Water[a]=self.Water[a].upper()
               if (((self.Water[a]).find(aranan))>=0):
                   self.pokemonisimleri.insert(a,self.Water[a])
               a=a+1  

    def Pokemon_veri(self):
        self.secilen=self.pokemonisimleri.selection_get()
        pokeozellikleri=pickle.load(open("pokemonlar.pkl","rb"))
        secilenpokemon=(pokeozellikleri[self.secilen])
        poke_resim_url=secilenpokemon['ResimURL']
        istek = requests.get(poke_resim_url)
        baglanti = istek.content
        self.cv = Canvas(bg='red')
        self.Resim = Image.open(BytesIO(baglanti))
        self.Resim=resizeimage.resize_cover( self.Resim, [210, 210], validate=False)
        self.image = ImageTk.PhotoImage(self.Resim)
        self.cv.grid(row=2,column=7,sticky="ns",rowspan=9,columnspan=5)
        self.cv.create_image(210, 210, image=self.image, anchor='center')
        self.pokemonadi=Label(text=(self.secilen)).grid(row=0,column=9,sticky="we")
        self.pokemonnumarasi=Label(text=(secilenpokemon['pokeno'])).grid(row=1,column=9,sticky="we")
        self.uzunluk=Label(text='Height: '+(secilenpokemon['Height'])).grid(row=12,column=9,sticky="we")
        self.agirlik=Label(text='Weight: '+(secilenpokemon['Weight'])).grid(row=13,column=9,sticky="we")
        self.katogori=Label(text='Category: '+(secilenpokemon['Category'])).grid(row=14,column=9,sticky="we")
        self.ozellik=Label(text='Abilities: '+(secilenpokemon['Abilities'])).grid(row=15,column=9,sticky="we")
        zayiflik=(secilenpokemon['Weaknesses'])
        if(len(zayiflik)==1):
            self.ozellik=Label(text='Weaknesses: '+(zayiflik[0])).grid(row=16,column=9,sticky="we")
        elif(len(zayiflik)==2):
            self.ozellik=Label(text='Weaknesses: '+(zayiflik[0])+','+(zayiflik[1])).grid(row=16,column=9,sticky="we")
        elif(len(zayiflik)==3):
            self.ozellik=Label(text='Weaknesses: '+(zayiflik[0])+','+(zayiflik[1])+','+(zayiflik[2])).grid(row=16,column=9,sticky="we")
        elif(len(zayiflik)==4):
            self.ozellik=Label(text='Weaknesses: '+(zayiflik[0])+','+(zayiflik[1])+','+(zayiflik[2])+','+(zayiflik[3])).grid(row=16,column=9,sticky="we")
        elif(len(zayiflik)==5):
            self.ozellik=Label(text='Weaknesses: '+(zayiflik[0])+','+(zayiflik[1])+','+(zayiflik[2])+','+(zayiflik[3])+','+(zayiflik[4])).grid(row=16,column=9,sticky="we")                
if __name__=="__main__":
   MainWindow().mainloop()

