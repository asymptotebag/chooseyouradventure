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

inventory = {}

'''
rooms contains boolean values for each room
    - order of rooms is: Library, Dungeon, Kitchen, Pantry, Fridge, Garden
    - Foyer, Cage, and Oven are excluded because they are each only visited once
    - True means that the room has not been visited yet
    - False means that the room has already been visited
these values are used to determine whether or not to show a hint 

'''
rooms = [True, True, True, True, True, True]
      
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
        if total<7:
            if (str(item) in inventory):
                inventory[item] += 1
            else:
                inventory[item] = 1
            messagebox.showinfo("Confirmation", str(item)+" has been added to inventory")
        else: 
            messagebox.showinfo("Error","Too many items in inventory")
        
    # remove item from inventory
    def remove_item(self, item):
        if item in inventory:
            if inventory[item]==1:
                del inventory[item]
            else:
                inventory[item] -= 1
        else:
            messagebox.showinfo("Error", "Item does not exist in inventory")
    
    def show_map(self):
        t = tk.Toplevel(self)
        t.title('Map')
        
        im = PIL.Image.open('Game Map.png')
        ima = PIL.ImageTk.PhotoImage(im)
        label = tk.Label(t, image = ima).pack()
        label.image=ima
    
    def hansel(self):
        t = tk.Toplevel(self)
        t.title('Hansel and Gretel')
        
        im = PIL.Image.open('Hansel and Gretel.png')
        ima = PIL.ImageTk.PhotoImage(im)
        label = tk.Label(t, image = ima).pack()
        label.image=ima
        
    def inventory(self):
        t = tk.Toplevel(self)
        t.title('Inventory')
        
        tk.Label(t, text = 'Item').grid(row=0, column = 0, padx= 20, pady=20)
        tk.Label(t, text = 'Quantity').grid(row=0, column=1, padx= 20, pady=20)
                    
        
    def potions(self):
        t = tk.Toplevel(self)
        t.title('Potent Potions')
        
        im = PIL.Image.open('Potent Potions.png')
        ima = PIL.ImageTk.PhotoImage(im)
        label = tk.Label(t, image = ima).pack()
        label.image=ima


# initialize start location (foyer) and widgets

class Welcome(tk.Frame):
    def __init__(self, master):
        master.geometry("960x720")
        tk.Frame.__init__(self, master)
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Welcome.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo

               
        pl = PIL.Image.open('play.png')
        pl = pl.resize((67,67))
        start = PIL.ImageTk.PhotoImage(pl)
        play = tk.Button(self, image = start,background = "#fe0000", borderwidth=0,
                   command=lambda: master.switch_frame(Instructions))
        play.image = start
        play_window = w.create_window(740, 500, window = play)


class Instructions(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)    
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Instructions.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        cont = tk.Button(self, text = 'CONTINUE',
                   command=lambda: master.switch_frame(Intro))
        cont_window = w.create_window(480, 600, window = cont)
        
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

class Foyer(tk.Frame):
    def __init__(self, master):        
        tk.Frame.__init__(self, master)    
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Foyer.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        '''
        hint = PIL.Image.open('hint_foyer.png')
        hint = hint.resize((773,229))
        hin = PIL.ImageTk.PhotoImage(hint)
        h=tk.Label(w, image=hin)
        h.pack()
        '''
        door = tk.Button(self, text="Testing testing 1 2 3 ", #this is temporary for testing
                   command=lambda: master.switch_frame(Kitchen))
        door_window = w.create_window(500,300, window = door)
                   
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#9b5c27", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 60, window = quit, anchor  = 'nw')
        
        
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#b37d4b", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#b37d4b", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        chu = tk.Button(self, background = "#89430c", borderwidth=0, relief = 'flat', width = 6, height = 8, 
                   command=lambda: master.switch_frame(End))
        chu_window = w.create_window(2, 370, window = chu, anchor  = 'nw')
        
        candy = tk.Button(self, background = "#89430c", width =6, height = 8, borderwidth=0, relief = 'flat', padx=0,
                   command=lambda: master.switch_frame(Cage))
        candy_window = w.create_window(890, 370, window = candy, anchor  = 'nw')
# initialize Edit Filter screen and widgets
class Cage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #tk.Label(self, text = "Cage").grid(row = 0, column = 0, columnspan = 4)

                
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Cage.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
                
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#7f735d", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 60, window = quit, anchor  = 'nw')
        
        lock = PIL.Image.open('lock.png')
        lock = lock.resize((35,45))
        lock2 = PIL.ImageTk.PhotoImage(lock)
        lock3 = tk.Button(self, image = lock2, background = "#7d5b16", state = "disabled", borderwidth=0,
                            command = lambda: master.switch_frame(Library))
        lock3.image = lock2
        lock_window = w.create_window(595,310, window = lock3)
        
        key = False
        def have_key():
            key = True
            lock3["state"] = "normal"
         
        def search_metal():
            num = random.randint(1, 4)
            if num==1:
                have_key()
                messagebox.showinfo("You found the key! Let's get out of here!")
            else:
                messagebox.showinfo("Sorry, you didn't find the key. Try again?")
     
        metal = PIL.Image.open('metal.png')
        metal2 = PIL.ImageTk.PhotoImage(metal)
        metal3 = tk.Button(self, image = metal2, background = "#0a0907", borderwidth=0,
                            command = lambda: search_metal()) #PROBABILITY
        metal3.image = metal2
        metal_window = w.create_window(310,540, window = metal3)
        
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#0a0907", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#0a0907", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
                        
# prompted by Open Image button
class Library(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Library.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
                
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#9b5c27", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#7f735d", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#7f735d", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
             
        kitchen = tk.Button(self, background = "#783f04", borderwidth=0, relief = 'flat', width = 5, height = 9, 
                   command=lambda: master.switch_frame(Kitchen))
        kitchen_window = w.create_window(2, 350, window = kitchen, anchor  = 'nw')

        dungeon = tk.Button(self, background = "#783f04", borderwidth=0, relief = 'flat', width = 5, height = 9, 
                   command=lambda: master.switch_frame(Dungeon))
        dungeon_window = w.create_window(900, 350, window = dungeon, anchor  = 'nw')  
        
        
        yellow = tk.Button(self, background = "#dfed09", borderwidth=0, relief = 'flat', width = 2, height = 2, 
                   command=lambda: master.potions())
        yellow_window = w.create_window(660, 351, window = yellow, anchor  = 'nw')  
        
        red = tk.Button(self, background = "#c02b5b", borderwidth=0, relief = 'flat', width = 9, height = 1, pady=0, 
                   command=lambda: master.hansel())
        red_window = w.create_window(431, 423, window = red, anchor  = 'nw')  
        
        brown = tk.Button(self, background = "#895825", borderwidth=0, relief = 'flat', width = 2, height = 2, 
                   command=lambda: master.switch_frame(Dungeon))
        brown_window = w.create_window(716, 361, window = brown, anchor  = 'nw')                      
                                                              
# initialize Kitchen screen and widgets
class Kitchen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        ####
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Kitchen.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
                
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#9b5c27", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#e6c991", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#e6c991", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        fridge = tk.Button(self, background = "#E7E8EA", borderwidth = 0, width = 15, height = 10, 
                            command = lambda: master.switch_frame(Refrigerator))
        fridge_window = w.create_window(187, 370, window = fridge, anchor = 'nw')
        
        oven = tk.Button(self, background = "#E7E8EA", borderwidth = 0, width = 10, height = 3,
                            command = lambda: master.switch_frame(Oven))
        oven_window = w.create_window(480, 470, window = oven)
        
        pantry = PIL.Image.open('cabinets.png')
        cab = PIL.ImageTk.PhotoImage(pantry)
        cabinet = tk.Button(self, image = cab, background = "#e6c991", borderwidth=0,
                   command=lambda: master.switch_frame(Pantry))
        cabinet.image = cab
        cabinet_window = w.create_window(509, 174, window = cabinet, anchor = 'nw')
            
        #### REPLACE DOORS
        garden = tk.Button(self, background = "#783f04", borderwidth=0, relief = 'flat', width = 5, height = 9, 
                   command=lambda: master.switch_frame(Garden))
        garden_window = w.create_window(2, 350, window = garden, anchor  = 'nw')

        library = tk.Button(self, background = "#783f04", borderwidth=0, relief = 'flat', width = 5, height = 9, 
                   command=lambda: master.switch_frame(Library))
        library_window = w.create_window(900, 350, window = library, anchor  = 'nw')  
         
# initialize Edit Filter screen and widgets
class Pantry(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Pantry.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
                
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#9B5C27", borderwidth=0,
                   command=lambda: master.switch_frame(Kitchen))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#B27D4B", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#B27D4B", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)

class Refrigerator(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Refrigerator.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
                
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#CCCCCC", borderwidth=0,
                   command=lambda: master.switch_frame(Kitchen))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#EFEFEF", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#EFEFEF", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
                
class Oven(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Oven.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
                
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#9f9f9f", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#959595", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#959595", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
             
                  
# initialize Edit Logo screen and widgets        
class Dungeon(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Dungeon.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
                
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#1a0300", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#6c614f", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#6c614f", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
             
        library = tk.Button(self, background = "#523e2f", borderwidth=0, relief = 'flat', width = 5, height = 9, 
                   command=lambda: master.switch_frame(Library))
        library_window = w.create_window(2, 350, window = library, anchor  = 'nw')
        
        
        left = tk.Button(self, background = "#5C5C5C", borderwidth=0, relief = 'flat', width =9, height = 4, 
                   command=lambda: master.switch_frame(Library))
        left_window = w.create_window(229, 481, window = left, anchor  = 'nw')  
        
        midleft = tk.Button(self, background = "#454545", borderwidth=0, relief = 'flat', width = 9, height = 4,
                   command=lambda: master.switch_frame(Library))
        midleft_window = w.create_window(372, 454, window = midleft, anchor  = 'nw')  
        
        midright = tk.Button(self, background = "#545253", borderwidth=0, relief = 'flat', width = 9, height = 4, 
                   command=lambda: master.switch_frame(Library))
        midright_window = w.create_window(534, 478, window = midright, anchor  = 'nw')      
        
        right = tk.Button(self, background = "#30302F", borderwidth=0, relief = 'flat', width = 9, height = 4, 
                   command=lambda: master.switch_frame(Library))
        right_window = w.create_window(721, 458, window = right, anchor  = 'nw')    
        
class Dark(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
                
        dark = tk.Canvas(self, width=960, height=720)
        dark.pack()
        
        bgim = PIL.Image.new('RGB', (960,720))
        bg = PIL.ImageTk.PhotoImage(bgim)
        black = dark.create_image((0,0), image = bg, anchor = 'nw')
        dark.image = bg
        
        switch = tk.Button(self, text = 'CONGRATS ON FINDING \n THE LIGHT SWITCH', bg = 'black', bd = 0,
                  command=lambda: master.switch_frame(Library))
        switch_window = dark.create_window(603, 450, window = switch, anchor  = 'nw')

    
# initialize Garden screen                                                                                                                                                              
class Garden(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Garden.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
                
        ex = PIL.Image.open('quit.png')
        ex = ex.resize((100,100))
        q = PIL.ImageTk.PhotoImage(ex)
        quit = tk.Button(self, image = q, background = "#b9e2fb", borderwidth=0,
                   command=lambda: master.switch_frame(End))
        quit.image = q
        quit_window = w.create_window(10, 70, window = quit, anchor  = 'nw')
        
        
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#274e13", borderwidth=0,
                   command=lambda: master.show_map())
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#274e13", borderwidth=0,
                   command=lambda: master.show_inventory())
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
             
        kitchen = tk.Button(self, background = "#502902", borderwidth=0, relief = 'flat', width = 5, height = 9, 
                   command=lambda: master.switch_frame(Kitchen))
        kitchen_window = w.create_window(875, 425, window = kitchen, anchor  = 'nw')   
                  
class End(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = ' ').grid(row = 0, column = 0)
        tk.Label(self, text = ' ').grid(row = 1, column = 0)
        tk.Label(self, text = "Thanks for playing! See you another time.").grid(row = 3, column = 0) ##   
                                                                                                    
    
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()