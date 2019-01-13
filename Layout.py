import PIL
import os.path  
import PIL.ImageDraw            
import random
import PIL.ImageFont  
import tkinter as tk
from PIL import ImageTk 

bag = []
      
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Foyer)

    # switching between screens
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()   
        
# initialize start location (foyer) and widgets
class Foyer(tk.Frame):
    def __init__(self, master):
        master.geometry("960x720")
        tk.Frame.__init__(self, master)
        
        
        w = tk.Canvas(self, width=960, height=720)
        w.pack()
        
        im = PIL.Image.open('Foyer.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        door = tk.Button(self, text="Testing testing 1 2 3 ", #this is temporary for testing
                   command=lambda: master.switch_frame(Dark))
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
                   command=lambda: master.switch_frame(Map))
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#b37d4b", borderwidth=0,
                   command=lambda: master.switch_frame(Backpack))
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        clock = PIL.Image.open('clock.png')
        clock = clock.resize((100,100))
        time = PIL.ImageTk.PhotoImage(clock)
        timer = tk.Button(self, image = time, background = "#9b5c27", borderwidth=0,
                   command=lambda: master.switch_frame(Timer))
        timer.image = time
        timer_window = w.create_window(850, 60, window = timer, anchor  = 'nw')
        
        chu = tk.Button(self, background = "#89430c", borderwidth=0, relief = 'flat', width = 6, height = 8, 
                   command=lambda: master.switch_frame(End))
        chu_window = w.create_window(2, 370, window = chu, anchor  = 'nw')
        
        candy = tk.Button(self, text = 'FREE\nCANDY\nHERE', background = "#89430c", width =6, height = 8, borderwidth=0, relief = 'flat', padx=0,
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
        
        
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#0a0907", borderwidth=0,
                   command=lambda: master.switch_frame(Map))
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#0a0907", borderwidth=0,
                   command=lambda: master.switch_frame(Backpack))
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        clock = PIL.Image.open('clock.png')
        clock = clock.resize((100,100))
        time = PIL.ImageTk.PhotoImage(clock)
        timer = tk.Button(self, image = time, background = "#7f735d", borderwidth=0,
                   command=lambda: master.switch_frame(Timer))
        timer.image = time
        timer_window = w.create_window(850, 60, window = timer, anchor  = 'nw')
        
        lock = tk.Button(self, text="Pick Lock",
                  command=lambda: master.switch_frame(Library))
        lock_window = w.create_window(400, 400, window = lock)
                        
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
                   command=lambda: master.switch_frame(Map))
        loc.image = pos
        loc_window = w.create_window(70, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#7f735d", borderwidth=0,
                   command=lambda: master.switch_frame(Backpack))
        inv.image = pack
        inv_window = w.create_window(850, 650, window = inv)
        
        clock = PIL.Image.open('clock.png')
        clock = clock.resize((100,100))
        time = PIL.ImageTk.PhotoImage(clock)
        timer = tk.Button(self, image = time, background = "#9b5c27", borderwidth=0,
                   command=lambda: master.switch_frame(Timer))
        timer.image = time
        timer_window = w.create_window(850, 70, window = timer, anchor  = 'nw')
             
        kitchen = tk.Button(self, background = "#783f04", borderwidth=0, relief = 'flat', width = 5, height = 9, 
                   command=lambda: master.switch_frame(Kitchen))
        kitchen_window = w.create_window(2, 350, window = kitchen, anchor  = 'nw')

        dungeon = tk.Button(self, background = "#783f04", borderwidth=0, relief = 'flat', width = 5, height = 9, 
                   command=lambda: master.switch_frame(Dungeon))
        dungeon_window = w.create_window(900, 350, window = dungeon, anchor  = 'nw')  
        
                          
                                                              
# initialize Kitchen screen and widgets
class Kitchen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        tk.Label(self, text = "Kitchen").grid(row = 0, column = 0, columnspan = 5)
        
        tk.Button(self, text="Library",
            command=lambda: master.switch_frame(Library)).grid(row=8, column = 0, columnspan = 5, sticky = "WE")
        tk.Button(self, text="Pantry",
                  command=lambda: master.switch_frame(Pantry)).grid(row=9, column = 0, columnspan = 5, sticky = "WE")
        tk.Button(self, text="Garden",
                  command=lambda: master.switch_frame(Garden)).grid(row=10, column = 0, columnspan = 5, sticky = "WE")
        tk.Button(self, text="Oven",
                  command=lambda: master.switch_frame(Oven)).grid(row=11, column = 0, columnspan = 5, sticky = "WE")
                                  
# initialize Edit Filter screen and widgets
class Pantry(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Pantry").grid(row = 0, column = 0, columnspan = 4)
        
        tk.Button(self, text="Kitchen",
                  command=lambda: master.switch_frame(Kitchen)).grid(row = 2, column = 0, columnspan = 4, sticky = "WE")
                  
class Oven(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Oven").grid(row = 0, column = 0, columnspan = 4)
        
        tk.Button(self, text="Kitchen",
                  command=lambda: master.switch_frame(Kitchen)).grid(row = 2, column = 0, columnspan = 4, sticky = "WE")
                  
# initialize Edit Logo screen and widgets        
class Dungeon(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Dungeon").grid(row = 0, column = 0, columnspan = 4)
        tk.Button(self, text="Library",
                  command=lambda: master.switch_frame(Library)).grid(row = 9, column = 0, columnspan = 4, sticky = "WE")

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
        tk.Label(self, text = "Garden").grid(row = 0, column = 0) ##
        
        tk.Button(self, text="Kitchen",
                  command=lambda: master.switch_frame(Kitchen)).grid(row = 3, column = 0, columnspan = 4, sticky = "WE")   
                  
class End(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = ' ').grid(row = 0, column = 0)
        tk.Label(self, text = ' ').grid(row = 1, column = 0)
        tk.Label(self, text = "Thanks for playing").grid(row = 3, column = 0) ##   
        
class Map(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Map").grid(row = 0, column = 0) ##    
        
class Backpack(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Inventory").grid(row = 0, column = 0) ##    

class Timer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Time is running out!").grid(row = 0, column = 0) ##                                                                                                        

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()