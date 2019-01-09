import PIL
import os.path  
import PIL.ImageDraw            
import random
import PIL.ImageFont  
import tkinter as tk
from tkinter.filedialog import askopenfilename,askdirectory
from PIL import ImageTk 
from PIL import ImageFilter

   
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
        
        im = PIL.Image.open('library.png')
        photo = PIL.ImageTk.PhotoImage(im)
        screen = w.create_image((0,0), image = photo, anchor = 'nw')
        w.image = photo
        
        door = tk.Button(self, text="Exit through the front door",
                   command=lambda: master.switch_frame(End))
        door_window = w.create_window(100,100, window = door)
                   
        quit = tk.Button(self, text = "QUIT", bg='#073763', fg = 'white', bd = 0, height = 2, width = 4,
                   command = lambda: master.switch_frame(End))
        quit_window = w.create_window(30,30, window = quit)
        
        position = PIL.Image.open('map.png')
        position = position.resize((70,90))
        pos = PIL.ImageTk.PhotoImage(position)
        loc = tk.Button(self, image = pos,background = "#3d85c6", borderwidth=0,
                   command=lambda: master.switch_frame(Cage))
        loc.image = pos
        loc_window = w.create_window(60, 650, window = loc)
        
        back = PIL.Image.open('backpack.png')
        back = back.resize((85,100))
        pack = PIL.ImageTk.PhotoImage(back)
        inv = tk.Button(self, image = pack, background = "#3d85c6", borderwidth=0,
                   command=lambda: master.switch_frame(Cage))
        inv.image = pack
        inv_window = w.create_window(830, 590, window = inv, anchor  = 'nw')
        
        clock = PIL.Image.open('clock.png')
        clock = clock.resize((100,100))
        time = PIL.ImageTk.PhotoImage(clock)
        timer = tk.Button(self, image = time, background = "#9fc5e8", borderwidth=0,
                   command=lambda: master.switch_frame(Cage))
        timer.image = time
        timer_window = w.create_window(860, 20, window = timer, anchor  = 'nw')
        
        ex = PIL.Image.open('exit.png')
        ex = ex.resize((50,50))
        out = PIL.ImageTk.PhotoImage(ex)
        chu = tk.Button(self, image = out, background = "#6fa8dc", borderwidth=0, relief = 'flat',
                   command=lambda: master.switch_frame(End))
        chu.image = out
        chu_window = w.create_window(15, 450, window = chu, anchor  = 'nw')
        
        candy = tk.Button(self, text = 'FREE CANDY \n THROUGH HERE', background = "#6fa8dc", borderwidth=0, relief = 'flat',
                   command=lambda: master.switch_frame(Cage))
        candy_window = w.create_window(705, 450, window = candy, anchor  = 'nw')
        
# initialize Edit Filter screen and widgets
class Cage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Cage").grid(row = 0, column = 0, columnspan = 4)

        tk.Button(self, text="Pick Lock",
                  command=lambda: master.switch_frame(Library)).grid(row = 2, column = 0, columnspan = 4, sticky = "WE")
 
                        
# prompted by Open Image button
class Library(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Library").grid(row = 0, column = 0) ##
        
        tk.Button(self, text="Kitchen",
                  command=lambda: master.switch_frame(Kitchen)).grid(row = 2, column = 0, columnspan = 4, sticky = "WE")
                  
        tk.Button(self, text="Dungeon",
                  command=lambda: master.switch_frame(Dungeon)).grid(row = 3, column = 0, columnspan = 4, sticky = "WE")         
                                
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
        tk.Label(self, text = "Thanks for playing").grid(row = 0, column = 0) ##                                                          

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()