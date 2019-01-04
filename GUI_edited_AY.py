import tkinter as tk
import PIL
from tkinter.filedialog import askopenfilename
from PIL import ImageTk 

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        master.geometry("600x600")
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Home Page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Open Image",
                   command=lambda: master.switch_frame(Image)).pack()
                  
        tk.Button(self, text="Edit Border",
                  command=lambda: master.switch_frame(Border)).pack()
        
        tk.Button(self, text="Edit Filter",
                  command=lambda: master.switch_frame(Filter)).pack()
                  
        tk.Button(self, text="Edit Logo",
                  command=lambda: master.switch_frame(Logo)).pack()
        
        tk.Button(self, text="Edit Text",
                  command=lambda: master.switch_frame(Text)).pack()
                  
class Border(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Border").grid(row = 0, column = 1, columnspan = 2)
        tk.Label(self, text = "Color").grid(row = 1, column = 0, columnspan = 2)
        tk.Label(self, text = "Style").grid(row = 1, column = 2, columnspan = 2)
        
        borderColor= tk.IntVar()
        tk.Radiobutton(self, text = "Red", variable=borderColor, value = 0).grid(row = 2, column = 0, sticky = "W")
        tk.Radiobutton(self, text = "Orange", variable=borderColor, value = 1).grid(row = 2, column = 1, sticky = "W")
        tk.Radiobutton(self, text = "Yellow", variable=borderColor, value = 2).grid(row = 3, column = 0, sticky = "W")
        tk.Radiobutton(self, text = "Green", variable=borderColor, value = 3).grid(row = 3, column = 1, sticky = "W")
        tk.Radiobutton(self, text = "Blue", variable=borderColor, value = 4).grid(row = 4, column = 0, sticky = "W")
        tk.Radiobutton(self, text = "Purple", variable=borderColor, value = 5).grid(row = 4, column = 1, sticky = "W")
        tk.Radiobutton(self, text = "Black", variable=borderColor, value = 6).grid(row = 5, column = 0, sticky = "W")
        tk.Radiobutton(self, text = "Brown", variable=borderColor, value = 7).grid(row = 5, column = 1, sticky = "W")
        
        style=tk.IntVar()
        tk.Radiobutton(self, text = "Style 1", variable=style, value = 0).grid(row = 2, column = 2, rowspan = 2)
        tk.Radiobutton(self, text = "Style 2", variable=style, value = 1).grid(row = 2, column = 3, rowspan = 2)
        tk.Radiobutton(self, text = "Style 3", variable=style, value = 2).grid(row = 4, column = 2, rowspan = 2)
        tk.Radiobutton(self, text = "Style 4", variable=style, value = 3).grid(row = 4, column = 3, rowspan = 2)
        
        tk.Label(self, text = "Width").grid(row = 6, column = 0, columnspan = 4)
        
        width = tk.Scale(self, from_=10, to=40, orient = "horizontal")
        width.grid(row=7, column = 0, columnspan = 4, sticky = "WE")
        
        tk.Button(self, text="Options",
                  command=lambda: master.switch_frame(StartPage)).grid(row=8, column = 0, columnspan = 4, sticky = "WE")
        
        
class Filter(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Filter").grid(row = 0, column = 1, columnspan = 2)
        
        #add the filter values to a list if they are clicked, offvalue is automatically set to 0
        
        f1=tk.IntVar()
        f2=tk.IntVar()
        f3=tk.IntVar()
        f4=tk.IntVar()
        
        tk.Checkbutton(self, text = "Filter 1", variable=f1, onvalue = 1).grid(row = 1, column = 0)
        tk.Checkbutton(self, text = "Filter 2", variable=f2, onvalue = 2).grid(row = 1, column = 1)
        tk.Checkbutton(self, text = "Filter 3", variable=f3, onvalue = 3).grid(row = 1, column = 2) 
        tk.Checkbutton(self, text = "Filter 4", variable=f4, onvalue = 4).grid(row = 1, column = 3) 
        
        tk.Button(self, text="Options",
                  command=lambda: master.switch_frame(StartPage)).grid(row = 2, column = 0, columnspan = 4, sticky = "WE")
                  
class Logo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Logo").grid(row = 0, column = 1, columnspan = 2)
        
        logoLoc=tk.IntVar()
        tk.Radiobutton(self, text = "Upper Left", variable=logoLoc, value = 0).grid(row = 1, column = 0, columnspan=2, sticky='W')
        tk.Radiobutton(self, text = "Lower Left", variable=logoLoc, value = 1).grid(row = 2, column = 0, columnspan=2, sticky='W')
        tk.Radiobutton(self, text = "Upper Right", variable=logoLoc, value = 2).grid(row = 1, column = 2, columnspan=2, sticky='W')
        tk.Radiobutton(self, text = "Lower Right", variable=logoLoc, value = 3).grid(row = 2, column = 2, columnspan=2, sticky='W') 
        
        tk.Button(self, text="Options",
                  command=lambda: master.switch_frame(StartPage)).grid(row = 3, column = 0, columnspan = 4, sticky = "WE")
                  
class Text(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Text").grid(row = 0, column = 1, columnspan = 2)
        
        font=tk.StringVar()
        tk.Radiobutton(self, text = "Arial", variable=font, value = 'arial').grid(row = 1, column = 0)
        tk.Radiobutton(self, text = "Times New Roman", variable=font, value = 'times new roman').grid(row = 1, column = 1)
        tk.Radiobutton(self, text = "Impact", variable=font, value = 'impact').grid(row = 1, column = 2) 
        tk.Radiobutton(self, text = "This", variable=font, value = 'this').grid(row = 1, column = 3) 
        
        e=tk.Entry(self)
        e.grid(row = 2, column = 0, columnspan = 4)
        e.insert(0,'Type your message here')
        
        tk.Button(self, text="Options",
                  command=lambda: master.switch_frame(StartPage)).grid(row = 5, column = 0, columnspan = 4, sticky = "WE")

class Image(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Image").grid(row = 0, column = 0)
        
        filename = askopenfilename()
        im=PIL.Image.open(filename)
        photo=PIL.ImageTk.PhotoImage(im)
        imageLabel = tk.Label(self, image=photo)
        imageLabel.grid(row=2, column=0)
        imageLabel.image=photo
        tk.Button(self, text="Options",
                  command=lambda: master.switch_frame(StartPage)).grid(row = 3, column = 0, columnspan = 4, sticky = "WE")
                                        
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()