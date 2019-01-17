import PIL
import os.path  
import PIL.ImageDraw            
import random
import PIL.ImageFont  
import tkinter as tk
from PIL import ImageTk 
import time
from tkinter import messagebox
import random

#dictionary of items in the inventory
inventory = {'hello':1, 'world': 2}

#the number of times that the cauldron has been stirred
num_stirs=[0]

#dictionary of items added to the cauldron
cauldron_items={}

#dictionary of the recipe for the potion
recipe={'ashes (1 tbsp)':8, 'curdled blood':1, "troll's hair":2, 'plastic plant leaves':10, 'tears':1,'paprika':1, 'black pepper':1}

'''
first_vis = list containing boolean values for each room
    - order of first_vis is: Library, Troll, Dungeon, Kitchen, Garden
    - Foyer, Cage, and Oven are excluded because they are each only visited once
    - Some rooms don't have hints
    - True means that the room has not been visited yet
    - False means that the room has already been visited
these values are used to determine whether or not to show a hint 

'''
first_vis = [True, True, True, True, True]
      
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Welcome)

    # switching between screens
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack() 
        
    # add item to inventory      
    def add_item(self, item):
        total = 0
        for i in inventory:
            total = total + inventory[i]
        if total<15: #max amount is 15
            if (str(item) in inventory):
                inventory[item] += 1
            else:
                inventory[item] = 1
            #message for successful addition
            messagebox.showinfo("Item added", str(item)+" has been added to your backpack.")
        else: #message if backpack is full
            messagebox.showinfo("Error","Backpack is full. Remove some items before adding more!")
        
    # remove item from inventory
    def remove_item(self, item, trade = False, cauld = False):
        #item = item.lower()
        item = item.strip()
        
        if item in inventory:
            if inventory[item]==1:
                del inventory[item]
            else:
                inventory[item] -= 1
            
            #if trade is true, the item is being given to the troll --> different message
            #user is transported to the dungeon
            #if a book was given, troll's hair is received in return
            if trade: 
                messagebox.showinfo("Trade Confirmed","Item \"" +item+"\" was successfully traded with the troll. You can now access the dungeon!")
                self.switch_frame(Dungeon) 
                if not item.islower(): 
                    self.add_item("troll's hair")
            
            #if cauld is true, the item is being added to the cauldron --> different message
            #item is added to cauldron_items
            #items in cauldron is displayed
            if cauld:
                if (str(item) in cauldron_items):
                    cauldron_items[item] += 1
                else:
                    cauldron_items[item] = 1
                messagebox.showinfo("Confirmation","Item \"" +item+"\" was successfully added to the cauldron.")
                self.show_cauldron()
            else: #basic remove item
                messagebox.showinfo("Item Removed","Item \"" +item+"\" was removed from your backpack.")
            self.show_inventory() #show inventory
        else:#if item is not in inventory, inform user
            messagebox.showinfo("Error", "Item \"" +item+"\" is not in your backpack!")
    
    #display the floor plan of the house
    def show_map(self):
        t = tk.Toplevel(self)
        t.title('Map')
        
        im = PIL.Image.open('Game Map.png')
        ima = PIL.ImageTk.PhotoImage(im)
        label = tk.Label(t, image = ima).pack()
        label.image=ima
    
    #display the book Hansel and Gretel
    def hansel(self):
        self.add_item("Hansel and Gretel")
        t = tk.Toplevel(self)
        t.title('Hansel and Gretel')
        
        im = PIL.Image.open('Hansel and Gretel.png')
        ima = PIL.ImageTk.PhotoImage(im)
        label = tk.Label(t, image = ima).pack()
        label.image=ima
        
    #display a potions book, with a recipe for strength potion
    def potions(self):
        self.add_item("Potent Potions")
        t = tk.Toplevel(self)
        t.title('Potent Potions')
        
        im = PIL.Image.open('Potent Potions.png')
        ima = PIL.ImageTk.PhotoImage(im)
        label = tk.Label(t, image = ima).pack()
        label.image=ima
            
    #display the inventory items
    def show_inventory(self):
        t = tk.Toplevel(self)
        t.title('Inventory')
        
        #items are displayed in two columns, w/ item name on left and quantity on right
        tk.Label(t, text = 'Item').grid(row=0, column = 0, padx= 20, pady=20)
        tk.Label(t, text = 'Quantity').grid(row=0, column=1, padx= 20, pady=20)
        
        items = ''
        quantities = ''
        for i in inventory: 
            items = items + i + '\n'
            quantities = quantities + str(inventory[i]) +'\n'
        tk.Label(t, text = items).grid(row=1, column = 0)
        tk.Label(t, text = quantities).grid(row=1, column = 1)            
        
        tk.Label(t, text = '').grid(row = 2, column = 0, columnspan = 2)
        
        
        #option to delete an item from your inventory by typing the name
        e=tk.Entry(t)
        e.grid(row = 3, column = 0, columnspan = 2)
        e.insert(0,'item to delete')
        
        tk.Button(t, text = 'DELETE ITEM',
                   command=lambda: self.remove_item(e.get())).grid(row = 4, column = 0, columnspan =  2)
    
    '''perform a trade with the troll
            - displays inventory
            - type item name to trade item
    '''
    def trade(self):
        t = tk.Toplevel(self)
        t.title('Inventory')
        
        tk.Label(t, text = 'Item').grid(row=0, column = 0, padx= 20, pady=20)
        tk.Label(t, text = 'Quantity').grid(row=0, column=1, padx= 20, pady=20)
        
        items = ''
        quantities = ''
        for i in inventory: 
            items = items + i + '\n'
            quantities = quantities + str(inventory[i]) +'\n'
        tk.Label(t, text = items).grid(row=1, column = 0)
        tk.Label(t, text = quantities).grid(row=1, column = 1)            
        
        tk.Label(t, text = '').grid(row = 2, column = 0, columnspan = 2)
        
        e=tk.Entry(t)
        e.grid(row = 3, column = 0, columnspan = 2)
        e.insert(0, 'trade item for entry')
        
        tk.Button(t, text = 'TRADE ITEM',
                   command=lambda: self.remove_item(e.get(), True)).grid(row = 4, column = 0, columnspan =  2)
    
    '''add an item to the cauldron
            - displays inventory
            - allows user to type item name and add to cauldron
    '''              
    def add_to_cauldron(self):
        t = tk.Toplevel(self)
        t.title('Inventory')
        
        tk.Label(t, text = 'Item').grid(row=0, column = 0, padx= 20, pady=20)
        tk.Label(t, text = 'Quantity').grid(row=0, column=1, padx= 20, pady=20)
        
        items = ''
        quantities = ''
        for i in inventory: 
            items = items + i + '\n'
            quantities = quantities + str(inventory[i]) +'\n'
        tk.Label(t, text = items).grid(row=1, column = 0)
        tk.Label(t, text = quantities).grid(row=1, column = 1)            
        
        tk.Label(t, text = '').grid(row = 2, column = 0, columnspan = 2)
        
        e=tk.Entry(t)
        e.grid(row = 3, column = 0, columnspan = 2)
        e.insert(0, 'add item to cauldron')
        
        tk.Button(t, text = 'ADD ITEM',
                   command=lambda: self.remove_item(e.get(), False, True)).grid(row = 4, column = 0, columnspan =  2)
    
    #displays items in the cauldron, which can not be removed  
    def show_cauldron(self):
        t = tk.Toplevel(self)
        t.title('Cauldron')
        
        tk.Label(t, text = 'Item').grid(row=0, column = 0, padx= 20, pady=20)
        tk.Label(t, text = 'Quantity').grid(row=0, column=1, padx= 20, pady=20)
        
        items = ''
        quantities = ''
        for i in cauldron_items: 
            items = items + i + '\n'
            quantities = quantities + str(cauldron_items[i]) +'\n'
        tk.Label(t, text = items).grid(row=1, column = 0)
        tk.Label(t, text = quantities).grid(row=1, column = 1)            
        
        tk.Label(t, text = '').grid(row = 2, column = 0, columnspan = 2)                                                                    
        


# initialize Welcome screen, with introduction to the game
class Welcome(tk.Frame):
    def __init__(self, master):
        master.geometry("960x720")
        tk.Frame.__init__(self, master)
        
        #set up canvas
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        #display welcome screen image as background
        im = PIL.Image.open('Welcome.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo

        #play button: click to progress       
        pl = PIL.Image.open('play.png')
        pl = pl.resize((67,67))
        start = PIL.ImageTk.PhotoImage(pl)
        play = tk.Button(self, image = start,background = "#fe0000", borderwidth=0,
                   command=lambda: master.switch_frame(Instructions))
        play.image = start
        play_window = w.create_window(740, 500, window = play)

# initialize Instructions screen
class Instructions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)    
        
        #set up canvas
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        #background
        im = PIL.Image.open('Instructions.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        #click button to proceed
        cont = tk.Button(self, text = 'CONTINUE',
                   command=lambda: master.switch_frame(Kitchen))
        cont_window = w.create_window(480, 600, window = cont)
 
#initialize Intro screen, with character and game background               
class Intro(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)    
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Prologue.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        cont = tk.Button(self, text = 'ENTER',
                   command=lambda: master.switch_frame(Foyer))
        cont_window = w.create_window(480, 600, window = cont)

#intitialize Foyer screen and widgets, starting point of game
class Foyer(tk.Frame):
    def __init__(self, master):        
        tk.Frame.__init__(self, master)    
        
        #set up canvas and background image
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Foyer.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        
        door = tk.Button(self, text="Testing testing 1 2 3 ", #this is temporary for testing
                   command=lambda: master.switch_frame(Library))
        door_window = w.create_window(500,300, window = door)
        

        #exit game      
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#9b5c27", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 60, window = quit, anchor  = 'nw')
        
        #view map
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#b37d4b", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        #view inventory
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#b37d4b", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        
        #set buttons to this image so sizes are in pixels
        clear = PIL.Image.open('clear.png')
        clr = PIL.ImageTk.PhotoImage(clear)
        
        #leave house
        chu = tk.Button(self, image= clr, background = "#89430c", borderwidth=0, relief = 'flat', width = 68, height = 225, 
                   command=lambda: master.switch_frame(End))
        chu.image = clr
        chu_window = w.create_window(2, 356, window = chu, anchor  = 'nw')
        
        #enter candy room (cage)
        candy = tk.Button(self, image = clr, background = "#89430c", width =68, height = 225, borderwidth=0, relief = 'flat', padx=0,
                   command=lambda: master.switch_frame(Cage))
        candy.image = clr
        candy_window = w.create_window(888, 356, window = candy, anchor  = 'nw')
        
# initialize Cage screen and widgets
class Cage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
                
        #set up canvas and background image
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Cage.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        
        #exit game        
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#7f735d", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 60, window = quit, anchor  = 'nw')
        
        #view map
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#0a0907", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        #view inventory
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#0a0907", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        
        #lock on cage, when opened, leads to Library
        lock = PIL.Image.open('lock.png')
        lock = lock.resize((35,45))
        lock2 = PIL.ImageTk.PhotoImage(lock)
        lock3 = tk.Button(self, image = lock2, background = "#7d5b16", state = "disabled", borderwidth=0,
                            command = lambda: master.switch_frame(Library))
        lock3.image = lock2
        lock_window = w.create_window(595,310, window = lock3)
        
        #if the user has the key, the lock can be opened
        key = False
        def have_key():
            key = True
            lock3["state"] = "normal"
        
        #search the metal for the key  
        def search_metal():
            num = random.randint(1, 4) #random chance of finding it
            if num==1:
                have_key()
                messagebox.showinfo("Congratulations!","You found the key! Pick the lock and get out of here!")
            else:
                messagebox.showinfo("Sorry", "Oops, you didn't find the key. Wallow in self-pity or try again?")   
        
        #pile of scrap metal, click to search 
        metal = PIL.Image.open('metal.png')
        metal2 = PIL.ImageTk.PhotoImage(metal)
        metal3 = tk.Button(self, image = metal2, background = "#0a0907", borderwidth=0,
                            command = lambda: search_metal()) #PROBABILITY
        metal3.image = metal2
        metal_window = w.create_window(310,540, window = metal3)
        
        #fish bone, add to inventory
        fishie = PIL.Image.open('fish.png')
        fishie = fishie.resize((50,50))
        fishy = PIL.ImageTk.PhotoImage(fishie)
        fish = tk.Button(self, image = fishy,background = "#0a0907", borderwidth=0,
                   command=lambda: master.add_item("fish"))
        fish.image = fishy
        fish_window = w.create_window(100, 575, window = fish)
        
        #cry, results in adding tears to inventory
        cr = PIL.Image.open('cry.png')
        cr = cr.resize((50,50))
        c = PIL.ImageTk.PhotoImage(cr)
        cry = tk.Button(self, image = c, background = "#7f735d", borderwidth=0,
                   command=lambda: master.add_item('tears'))
        cry.image = c
        cry_window = w.create_window(200,300 , window = cry)
                
#initiate Library screen and widgets
class Library(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #set up canvas and background
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Library.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        #if this is the first time the user is in the library, display hint
        if first_vis[0]:
            hint = PIL.Image.open('hint_library.png')
            hin = PIL.ImageTk.PhotoImage(hint)
            hi = tk.Label(self, image = hin, background = "#7f735d")
            hi.image = hin
            hi_window = w.create_window(214, 550, window = hi, anchor  = 'nw')
            
        #exit game
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#9b5c27", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        #view map
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#7f735d", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        #view inventory
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#7f735d", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
             
        #add to buttons so sizes are in pixels     
        clear = PIL.Image.open('clear.png')
        clr = PIL.ImageTk.PhotoImage(clear)
        
        #send the user to Dark if it's the first visit and they click the door to the kitchen
        if first_vis[3]:
            kitchen = tk.Button(self, image = clr, background = "#783f04", borderwidth=0, relief = 'flat', width = 57, height = 250, 
                   command=lambda: master.switch_frame(Dark))
        else:
            kitchen = tk.Button(self, image = clr, background = "#783f04", borderwidth=0, relief = 'flat', width = 57, height = 250, 
                   command=lambda: master.switch_frame(Kitchen))
        kitchen.image = clr
        kitchen_window = w.create_window(2, 338, window = kitchen, anchor  = 'nw')

        #send the user to Troll 
        dungeon = tk.Button(self, image = clr, background = "#783f04", borderwidth=0, relief = 'flat', width = 55, height = 248, 
                   command=lambda: master.switch_frame(Troll))
        dungeon.image = clr    
        dungeon_window = w.create_window(899, 338, window = dungeon, anchor  = 'nw')  
        
        #button for the yellow book (Potent Potions): read and add to inventory
        yellow = tk.Button(self, image = clr, background = "#dfed09", borderwidth=0, relief = 'flat', width = 18, height = 40, 
                   command=lambda: master.potions())
        yellow.image=clr
        yellow_window = w.create_window(661, 353, window = yellow, anchor  = 'nw')  
        
        #button for the red book (Hansel and Gretel): read and add to inventory
        red = tk.Button(self, image = clr, background = "#c02b5b", borderwidth=0, relief = 'flat', width = 63, height = 9, pady=0, 
                   command=lambda: master.hansel())
        red.image=clr
        red_window = w.create_window(431, 425, window = red, anchor  = 'nw')  
        
        #function for the Crucible, display message that the book is illegible
        def read_error():
            master.add_item('The Crucible')
            messagebox.showinfo(":(", "This book, \"The Crucible,\" is too blotched with tears to read!")
        
        #button for the brown book (The Crucible): read and add to inventory
        brown = tk.Button(self, image=clr, background = "#895825", borderwidth=0, relief = 'flat', width = 19, height = 38, 
                   command=lambda: read_error())
        brown.image=clr
        brown_window = w.create_window(716, 363, window = brown, anchor  = 'nw')                      
       
        #set first_vis value for Library to False
        first_vis[0]=False    
        
                                                                                                  
# initialize Kitchen screen and widgets
class Kitchen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #set up canvas and background
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Kitchen.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo

        #exit game            
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#9b5c27", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        #view map
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#e6c991", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        #view inventory
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#e6c991", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        #add to buttons so sizes are in pixels
        clear = PIL.Image.open('clear.png')
        clr = PIL.ImageTk.PhotoImage(clear)
        
        #button for Fridge screen
        fridge = tk.Button(self, image = clr, background = "#E7E8EA", borderwidth = 0, width = 121, height = 185, 
                            command = lambda: master.switch_frame(Refrigerator))
        fridge.image = clr
        fridge_window = w.create_window(188, 372, window = fridge, anchor = 'nw')
        
        #button for Oven screen
        oven = tk.Button(self, image = clr,  background = "#E7E8EA", borderwidth = 0, width = 90, height = 58,
                            command = lambda: master.switch_frame(Oven))
        oven.image = clr
        oven_window = w.create_window(432, 444, window = oven, anchor = 'nw')
        
        #button for pantry 
        pantry = PIL.Image.open('cabinets.png')
        cab = PIL.ImageTk.PhotoImage(pantry)
        cabinet = tk.Button(self, image = cab, background = "#e6c991", borderwidth=0,
                   command=lambda: master.switch_frame(Pantry))
        cabinet.image = cab
        cabinet_window = w.create_window(509, 174, window = cabinet, anchor = 'nw')
        
        #button for cauldron
        cauldron = tk.Button(self, image = clr,  background = "black", borderwidth = 0, width = 82, height = 65,
                            command = lambda: master.switch_frame(Cauldron))
        cauldron.image = clr
        cauldron_window = w.create_window(657, 490, window = cauldron, anchor = 'nw')
            
        #door to garden
        garden = tk.Button(self, image = clr, background = "#783f04", borderwidth=0, relief = 'flat', width = 57, height = 250, 
                   command=lambda: master.switch_frame(Garden))
        garden.image = clr
        garden_window = w.create_window(2, 338, window = garden, anchor  = 'nw')
        
        #door to library
        library = tk.Button(self, image = clr, background = "#783f04", borderwidth=0, relief = 'flat', width = 55, height = 248, 
                   command=lambda: master.switch_frame(Library))
        library.image = clr
        library_window = w.create_window(899, 338, window = library, anchor  = 'nw') 
        
        #set first_vis value for Kitchen to False
        first_vis[3]=False 
        
# initialize Pantry screen and widgets
class Pantry(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #set up canvas and background
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Pantry.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        #exit Pantry (return to Kitchen)       
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#9B5C27", borderwidth=0,
                   command=lambda: master.switch_frame(Kitchen))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        #view map
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#B27D4B", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        #view inventory
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#B27D4B", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        #buttons to add garlic, paprika, anise, cinnamon, and black pepper to inventory
        garlic = tk.Button(self, text = 'Choose Me', 
                   command=lambda: master.add_item('garlic'))
        garlic_window = w.create_window(242, 145, window = garlic, anchor  = 'nw')
        
        paprika = tk.Button(self, text = 'Choose Me', 
                   command=lambda: master.add_item('paprika'))
        paprika_window = w.create_window(440, 120, window = paprika, anchor  = 'nw')
        
        anise = tk.Button(self, text = 'Choose Me', 
                   command=lambda: master.add_item('anise'))
        anise_window = w.create_window(715, 103, window = anise, anchor  = 'nw')
        
        cinn = tk.Button(self, text = 'Choose Me', 
                   command=lambda: master.add_item('cinnamon'))
        cinn_window = w.create_window(285, 400, window = cinn, anchor  = 'nw')
        
        black = tk.Button(self, text = 'Choose Me', 
                   command=lambda: master.add_item('black pepper'))
        black_window = w.create_window(577, 388, window = black, anchor  = 'nw')

#initialize Refrigerator screen and widgets       
class Refrigerator(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #set up canvas and background
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Refrigerator.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        #exit Refrigerator (return to Kitchen)     
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#CCCCCC", borderwidth=0,
                   command=lambda: master.switch_frame(Kitchen))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        #view map
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#EFEFEF", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        #view inventory
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#EFEFEF", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        #buttons to add milk, cheese, and blood to inventory
        milk = tk.Button(self, text = 'Choose Me', 
                   command=lambda: master.add_item('milk'))
        milk_window = w.create_window(242, 145, window = milk)
        
        cheese = tk.Button(self, text = 'Choose Me', 
                   command=lambda: master.add_item('cheese'))
        cheese_window = w.create_window(478, 300, window = cheese)
        
        blood = tk.Button(self, text = 'Choose Me', 
                   command=lambda: master.add_item('curdled blood'))
        blood_window = w.create_window(695, 185, window = blood)
        
#initialize Oven screen and widgets               
class Oven(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #set up canvas and background
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Oven.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        #exit game               
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#9f9f9f", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        #view map
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#959595", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        #view inventory
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#959595", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)

#initialize Troll screen and widgets            
class Troll(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #set up canvas and background        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Troll.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        #if this is the first visit, display hint
        if first_vis[1]:
            hint = PIL.Image.open('hint_troll.png')
            hin = PIL.ImageTk.PhotoImage(hint)
            hi = tk.Label(self, image = hin, background = "black")
            hi.image = hin
            hi_window = w.create_window(680, 100, window = hi, anchor  = 'nw')
        
        #exit game
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#1a0300", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        #view map
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "black", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        #view inventory
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "black", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        #click on head of troll to trade
        head = PIL.Image.open('head.png')
        h = PIL.ImageTk.PhotoImage(head)
        troll = tk.Button(self, image = h, background = "black", borderwidth=0,
                   command=lambda: master.trade())
        troll.image = h
        troll_window = w.create_window(337, 70, window = troll, anchor = 'nw')
        
        #add to button so sizes are in pixels
        clear = PIL.Image.open('clear.png')
        clr = PIL.ImageTk.PhotoImage(clear)
        
        #return to library
        library = tk.Button(self, image= clr, background = "#523e2f", borderwidth=0, relief = 'flat', width = 55, height = 250, 
                   command=lambda: master.switch_frame(Library))
        library.image = clr
        library_window = w.create_window(2, 340, window = library, anchor  = 'nw')
        
        #set first_vis value for Troll to False
        first_vis[1]=False
                        
# initialize Dungeon screen and widgets        
class Dungeon(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #set up canvas and background
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Dungeon.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        #if this is the first visit, display hint        
        if first_vis[2]:
            hint = PIL.Image.open('hint_dungeon.png')
            hin = PIL.ImageTk.PhotoImage(hint)
            hi = tk.Label(self, image = hin, background = "#1a0300")
            hi.image = hin
            hi_window = w.create_window(480,80, window = hi)
            
        #exit game                    
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#1a0300", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        #view map
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#6c614f", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        #view inventory
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#6c614f", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        #add to button so sizes are in pixels
        clear = PIL.Image.open('clear.png')
        clr = PIL.ImageTk.PhotoImage(clear)
        
        #buttons to add bones or ashes to inventory when graves are clicked (all are bones except midleft, which is ashes)
        left = tk.Button(self, image = clr, background = "#5C5C5C", borderwidth=0, relief = 'flat', width =65, height = 75, 
                   command=lambda: master.add_item("bones"))
        left.image=clr
        left_window = w.create_window(229, 481, window = left, anchor  = 'nw')  
        
        midleft = tk.Button(self, image = clr, background = "#454545", borderwidth=0, relief = 'flat', width = 65, height = 75,
                   command=lambda: master.add_item("ashes (1 tbsp)"))
        midleft.image=clr
        midleft_window = w.create_window(372, 454, window = midleft, anchor  = 'nw')  
        
        midright = tk.Button(self, image = clr, background = "#545253", borderwidth=0, relief = 'flat',width = 70, height = 75,
                   command=lambda: master.add_item("bones"))
        midright.image = clr
        midright_window = w.create_window(534, 478, window = midright, anchor  = 'nw')      
        
        right = tk.Button(self, image = clr, background = "#30302F", borderwidth=0, relief = 'flat', width = 65, height = 75, 
                   command=lambda: master.add_item("bones"))
        right.image = clr
        right_window = w.create_window(721, 458, window = right, anchor  = 'nw')
        
        #return to library        
        library = tk.Button(self, image= clr, background = "#523e2f", borderwidth=0, relief = 'flat', width = 55, height = 250, 
                   command=lambda: master.switch_frame(Library))
        library.image = clr
        library_window = w.create_window(2, 340, window = library, anchor  = 'nw')   
        
        #set first_vis value for Dungeon to False
        first_vis[2]=False

#intialize Dark screen and widgets 
#must locate black button (light switch) to progress to Kitchen     
class Dark(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #set up canvas and background    
        dark = tk.Canvas(self, width=960, height=720)
        dark.pack()
        
        bgim = PIL.Image.new('RGB', (960,720))
        bg = PIL.ImageTk.PhotoImage(bgim)
        black = dark.create_image((0,0), image = bg, anchor = 'nw')
        dark.image = bg
        
        #show message that the room is too dark to see in
        messagebox.showinfo("Kitchen", "The next room is too dark to see in. You need to find the light switch on the wall.")
        
        #switch: click to enter Kitchen
        switch = tk.Button(self, text = '                \n\n\n\n', bg = 'black', bd = 0,
                  command=lambda: master.switch_frame(Kitchen))
        switch_window = dark.create_window(603, 450, window = switch, anchor  = 'nw')

    
# initialize Garden screen and widgets                                                                                                                                                              
class Garden(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #set up canvas and background
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Garden.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
       
        #if this is the first visit, display hint   
        if first_vis[4]:
            hint = PIL.Image.open('hint_garden.png')
            hin = PIL.ImageTk.PhotoImage(hint)
            hi = tk.Label(self, image = hin, background = "#274e13")
            hi.image = hin
            hi_window = w.create_window(233, 581, window = hi, anchor  = 'nw')
         
        #exit game           
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#b9e2fb", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        #view map
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#274e13", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        #view bag
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#274e13", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        
        #buttons to add plant leaves to inventory
        chooseshort = tk.Button(self, text = 'Choose Me',
                   command=lambda: master.add_item("short leaves"))
        chooseshort_window = w.create_window(160, 400, window = chooseshort)
        chooseyellow = tk.Button(self, text = 'Choose Me',
                   command=lambda: master.add_item("yellow flowers"))
        chooseyellow_window = w.create_window(315, 363, window = chooseyellow)
        choosepot = tk.Button(self, text = 'Choose Me',
                   command=lambda: master.add_item("potted plant"))
        choosepot_window = w.create_window(480, 190, window = choosepot)
        choosetall = tk.Button(self, text = 'Choose Me',
                   command=lambda: master.add_item("plastic plant leaves"))
        choosetall_window = w.create_window(667, 225, window = choosetall)
        
        #add to button so size is in pixels
        clear = PIL.Image.open('clear.png')
        clr = PIL.ImageTk.PhotoImage(clear)
        
        #return to kitchen
        kitchen = tk.Button(self, image = clr, background = "#502902", borderwidth=0, relief = 'flat', width = 58, height = 130, 
                   command=lambda: master.switch_frame(Kitchen))
        kitchen.image = clr
        kitchen_window = w.create_window(858, 432, window = kitchen, anchor  = 'nw')   
        
        #set first_vis value for Garden to False
        first_vis[4]=False    

#initialize Cauldron screen and widgets
class Cauldron(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        #set up canvas and background
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Cauldron.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
           
        #exit game     
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#990000", borderwidth=0,
                   command=lambda: master.switch_frame(Kitchen))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        #view map
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#990000", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        #view inventory
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#990000", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        #click on top of cauldron to add items to the cauldron
        top = PIL.Image.open('cauldronTop.png')
        ctop = PIL.ImageTk.PhotoImage(top)
        cauldronTop = tk.Button(self, image = ctop, background = "black", borderwidth=0,
                   command=lambda: master.add_to_cauldron())
        cauldronTop.image = ctop
        cauldronTop_window = w.create_window(480, 360, window = cauldronTop)
        
        #count the number of stirs (add 1)
        def count_stirs():
            num_stirs[0]+=1
        
        #determine whether or not the completed potion is correct
        def finish_potion():
            correct = True
            for i in recipe:
                if not (i in cauldron_items):
                    correct = False
                else:
                    if not (cauldron_items[i]==recipe[i]):
                        correct = False
            
            if not (num_stirs[0]==3):
                correct=False
                
            if correct:
                master.add_item('Draught for Ultimate Strength')
            else: 
                master.add_item('Draught of Ultimate Strength')
        
        #button to stir
        stir = tk.Button(self, text = 'Stir', 
                   command=lambda: count_stirs())
        stir_window = w.create_window(840, 145, window = stir, anchor  = 'nw')
        
        #finish the potion
        finish = tk.Button(self, text = 'Finish potion', 
                   command=lambda: finish_potion())
        finish_window = w.create_window(480, 640, window = finish)

#initialize End screen and widgets      
class End(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = ' ').grid(row = 0, column = 0)
        tk.Label(self, text = ' ').grid(row = 1, column = 0)
        tk.Label(self, text = "Quitting, are you? You would have died if it wasn't a game, you know!").grid(row = 3, column = 0) ##   

#intialize winning screen and widgets
class Win(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('win.jpg')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo)
        w.image = photo   

#initialize losing screen and widgets
class Lose(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Garden.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo                                                                                                                                                                                                                                                                                                                                                                                                     
    
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()