import PIL
import os.path  
import PIL.ImageDraw            
import random
import PIL.ImageFont  
import tkinter as tk
from PIL import ImageTk 
       
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    # switching between screens
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        

# initialize Home Page and widgets
class StartPage(tk.Frame):
    def __init__(self, master):
        master.geometry("600x600")
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Home Page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Open Image",
                   command=lambda: master.switch_frame(Kitchen)).pack()
                  
        
# initialize Edit Border screen and widgets
class Kitchen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        tk.Label(self, text = "Border").grid(row = 0, column = 0, columnspan = 5)
        tk.Label(self, text = "Color").grid(row = 1, column = 0, columnspan = 2)
        tk.Label(self, text = "Style").grid(row = 1, column = 3, columnspan = 2)
        
        #border color options
        borderColor= tk.IntVar()
        borderColor.set(-1)
        tk.Radiobutton(self, text = "Red", variable=borderColor, value = 0).grid(row = 2, column = 0, sticky = "W")
        tk.Radiobutton(self, text = "Orange", variable=borderColor, value = 1).grid(row = 2, column = 1, sticky = "W")
        tk.Radiobutton(self, text = "Yellow", variable=borderColor, value = 2).grid(row = 3, column = 0, sticky = "W")
        tk.Radiobutton(self, text = "Green", variable=borderColor, value = 3).grid(row = 3, column = 1, sticky = "W")
        tk.Radiobutton(self, text = "Blue", variable=borderColor, value = 4).grid(row = 4, column = 0, sticky = "W")
        tk.Radiobutton(self, text = "Purple", variable=borderColor, value = 5).grid(row = 4, column = 1, sticky = "W")
        tk.Radiobutton(self, text = "Black", variable=borderColor, value = 6).grid(row = 5, column = 0, sticky = "W")
        tk.Radiobutton(self, text = "Brown", variable=borderColor, value = 7).grid(row = 5, column = 1, sticky = "W")
        
        tk.Label(self, text ='     ').grid(row = 2, column = 2, columnspan = 1, rowspan=4)
        
        #border style options
        style=tk.IntVar()
        style.set(-1)
        tk.Radiobutton(self, text = "Rectangular ", variable=style, value = 0).grid(row = 2, column = 3, rowspan = 2)
        tk.Radiobutton(self, text = "Rounded", variable=style, value = 1).grid(row = 2, column = 4, rowspan = 2)
        tk.Radiobutton(self, text = "Double      ", variable=style, value = 2).grid(row = 4, column = 3, rowspan = 2)
        tk.Radiobutton(self, text = "Abstract", variable=style, value = 3).grid(row = 4, column = 4, rowspan = 2)
        
        tk.Label(self, text ='     ').grid(row = 6)
        
        tk.Label(self, text = "Width").grid(row = 7, column = 0, columnspan = 5)
        
        #border width
        width = tk.Scale(self, from_=10, to=40, orient = "horizontal")
        width.grid(row=8, column = 0, columnspan = 5, sticky = "WE")
        
        tk.Button(self, text="Options",
                  command=lambda: master.switch_frame(StartPage)).grid(row=9, column = 0, columnspan = 5, sticky = "WE")
        tk.Button(self, text="Set Border",
                  command=lambda: master.save_mods(3, (style.get(), float(width.get()/100.),borderColor.get()))).grid(row=10, column = 0, columnspan = 5, sticky = "WE")
        
# initialize Edit Filter screen and widgets
class Pantry(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Filter").grid(row = 0, column = 0, columnspan = 4)
        
        f1=tk.IntVar()
        f2=tk.IntVar()
        f3=tk.IntVar()
        f4=tk.IntVar()
        
        #filter options
        tk.Checkbutton(self, text = "Black and White", variable=f1, onvalue = 1).grid(row = 1, column = 0)
        tk.Checkbutton(self, text = "Sepia", variable=f2, onvalue = 2).grid(row = 1, column = 1)
        tk.Checkbutton(self, text = "Detail", variable=f3, onvalue = 3).grid(row = 1, column = 2) 
        tk.Checkbutton(self, text = "Smooth", variable=f4, onvalue = 4).grid(row = 1, column = 3) 
        
        tk.Button(self, text="Options",
                  command=lambda: master.switch_frame(StartPage)).grid(row = 2, column = 0, columnspan = 4, sticky = "WE")
        tk.Button(self, text="Set Filter(s)",
                  command=lambda: master.save_mods(0,(f1.get(),f2.get(),f3.get(),f4.get()))).grid(row=4, column = 0, columnspan = 4, sticky = "WE")
                    
# initialize Edit Logo screen and widgets        
class Basement(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text = "Logo").grid(row = 0, column = 1, columnspan = 2)
        
        #logo location options
        logoLoc=tk.IntVar()
        logoLoc.set(-1)
        tk.Radiobutton(self, text = "Upper Left", variable=logoLoc, value = 0).grid(row = 1, column = 0, columnspan=2, sticky='W')
        tk.Radiobutton(self, text = "Lower Left", variable=logoLoc, value = 1).grid(row = 2, column = 0, columnspan=2, sticky='W')
        tk.Radiobutton(self, text = "Upper Right", variable=logoLoc, value = 2).grid(row = 1, column = 2, columnspan=2, sticky='W')
        tk.Radiobutton(self, text = "Lower Right", variable=logoLoc, value = 3).grid(row = 2, column = 2, columnspan=2, sticky='W') 
        
        #logo color options
        tk.Label(self).grid(row = 3)
        logoColor= tk.IntVar()
        logoColor.set(-1)
        tk.Radiobutton(self, text = "Red", variable=logoColor, value = 0).grid(row = 4, column = 0, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Orange", variable=logoColor, value = 1).grid(row = 4, column = 2, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Yellow", variable=logoColor, value = 2).grid(row = 5, column = 0, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Green", variable=logoColor, value = 3).grid(row = 5, column = 2, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Blue", variable=logoColor, value = 4).grid(row = 6, column = 0,  columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Purple", variable=logoColor, value = 5).grid(row = 6, column = 2, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Black", variable=logoColor, value = 6).grid(row = 7, column = 0, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Brown", variable=logoColor, value = 7).grid(row = 7, column = 2, columnspan=2, sticky = "W")
           
        
        #display logo 
        im=PIL.Image.open('logo image.png')
        wid,hei=im.size
        rfactor=100./(max(wid,hei))
        im= im.resize((int(rfactor*wid), int(rfactor*hei)))
        
        photo=PIL.ImageTk.PhotoImage(im)
        imageLabel = tk.Label(self, image=photo)
        imageLabel.grid(row=8, column=1, columnspan=2)
        imageLabel.image=photo
        
        tk.Button(self, text="Options",
                  command=lambda: master.switch_frame(StartPage)).grid(row = 9, column = 0, columnspan = 4, sticky = "WE")
        tk.Button(self, text="Set Logo",
                  command=lambda: master.save_mods(1,(logoLoc.get(),logoColor.get()))).grid(row=10, column = 0, columnspan = 4, sticky = "WE")
                  
# initialize Edit Text screen and widgets                                
class Vault(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Text").grid(row = 0, column = 1, columnspan = 2)
        
        #text location options
        textLoc=tk.IntVar()
        textLoc.set(-1) 
        tk.Radiobutton(self, text = "Upper Left", variable=textLoc, value = 0).grid(row = 1, column = 0, columnspan=2, sticky='W')
        tk.Radiobutton(self, text = "Lower Left", variable=textLoc, value = 1).grid(row = 2, column = 0, columnspan=2, sticky='W')
        tk.Radiobutton(self, text = "Upper Right", variable=textLoc, value = 2).grid(row = 1, column = 2, columnspan=2, sticky='W')
        tk.Radiobutton(self, text = "Lower Right", variable=textLoc, value = 3).grid(row = 2, column = 2, columnspan=2, sticky='W') 
        
        tk.Label(self).grid(row=3)
        
        #text font options
        font=tk.StringVar()
        font.set('arial')
        tk.Radiobutton(self, text = "Arial", variable=font, value = 'arial').grid(row = 4, column = 0)
        tk.Radiobutton(self, text = "Times New Roman", variable=font, value = 'times').grid(row = 4, column = 1)
        tk.Radiobutton(self, text = "Impact", variable=font, value = 'impact').grid(row = 4, column = 2) 
        tk.Radiobutton(self, text = "Calibri", variable=font, value = 'calibri').grid(row = 4, column = 3) 
        
        tk.Label(self).grid(row = 5)
        
        #text color options
        textColor= tk.IntVar()
        textColor.set(-1)
        tk.Radiobutton(self, text = "Red", variable=textColor, value = 0).grid(row = 6, column = 0, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Orange", variable=textColor, value = 1).grid(row = 6, column = 2, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Yellow", variable=textColor, value = 2).grid(row = 7, column = 0, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Green", variable=textColor, value = 3).grid(row = 7, column = 2, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Blue", variable=textColor, value = 4).grid(row = 8, column = 0,  columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Purple", variable=textColor, value = 5).grid(row = 8, column = 2, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Black", variable=textColor, value = 6).grid(row = 9, column = 0, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Brown", variable=textColor, value = 7).grid(row = 9, column = 2, columnspan=2, sticky = "W")
        
        #text entry
        e=tk.Entry(self)
        e.grid(row = 10, column = 0, columnspan = 4)
        e.insert(0,'Type your message')
        
        #text size
        size = tk.Scale(self, from_=11, to=40, orient = "horizontal")
        size.grid(row=11, column = 0, columnspan = 4, sticky = "WE")
        
        tk.Button(self, text="Options",
                  command=lambda: master.switch_frame(StartPage)).grid(row = 13, column = 0, columnspan = 4, sticky = "WE")
        tk.Button(self, text="Set Text",
                  command=lambda: master.save_mods(2,(e.get(), size.get(),textLoc.get(), font.get(),textColor.get()))).grid(row=15, column = 0, columnspan = 4, sticky = "WE")

# prompted by Open Image button
class Library(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Image").grid(row = 0, column = 0) ##
        
        filename = askopenfilename()
        im=PIL.Image.open(filename)
        wid,hei=im.size
        rfactor=500./(max(wid,hei))
        im= im.resize((int(rfactor*wid), int(rfactor*hei)))
        
        photo=PIL.ImageTk.PhotoImage(im)
        imageLabel = tk.Label(self, image=photo)
        imageLabel.grid(row=2, column=0)
        imageLabel.image=photo
        
        
        tk.Button(self, text="Options",
                  command=lambda: master.switch_frame(StartPage)).grid(row = 3, column = 0, columnspan = 4, sticky = "WE")
                  
# prompted by FINALIZE button
class Cages(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Selections").grid(row = 0, column = 0, columnspan=2) ##
        tk.Label(self).grid(row = 1, column = 0) ##
        
        single=tk.BooleanVar()
        tk.Radiobutton(self, text = "Apply modifications to one image", variable=single, value = True).grid(row = 2, column = 0, columnspan=2, sticky = "W")
        tk.Radiobutton(self, text = "Apply modifications to multiple images", variable=single, value = False).grid(row = 3, column = 0, columnspan=2, sticky = "W")
        
        tk.Button(self, text="Proceed",
                  command=lambda: master.set_selection(single.get())).grid(row = 4, column = 0, columnspan = 4, sticky = "WE") 
        
# displays modified image                                                                                                                                                                
class Backyard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Finalize").grid(row = 0, column = 0) ##
        
        
        tk.Button(self, text="Return",
                  command=lambda: master.switch_frame(StartPage)).grid(row = 3, column = 0, columnspan = 4, sticky = "WE")                                                          

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()