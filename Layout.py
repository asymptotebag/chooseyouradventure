import PIL
import os.path  
import PIL.ImageDraw            
import PIL.ImageFont  
import tkinter as tk
from PIL import ImageTk 
       
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
        master.geometry("800x600")
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Foyer").pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Crying is a good way to relieve stress. We recommend you do it at least once.").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="FREE CANDY THROUGH HERE",
                   command=lambda: master.switch_frame(Cage)).pack()
                  
   
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

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()