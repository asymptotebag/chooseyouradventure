import PIL
import os.path  
import PIL.ImageDraw            
import random
import PIL.ImageFont  
import tkinter as tk
from tkinter.filedialog import askopenfilename,askdirectory
from PIL import ImageTk 
from PIL import ImageFilter

''' global variable: 
    - filter 
    - logo = (location, color)
    - text = (message, size, location, font, color)
    - border = (shape, border width, color)
'''
mods=[(0,0,0,0),(-1,-1),(-1,-1,-1,-1,-1),(-1,-1,-1)] 
change_one_only=[True]

def convert(num):
    #convert a color number to the rgb value
    
    colors=[(239,58,55),(244,131,61),(252,218,95),(80,145,50),(74,115,196),(145,51,204),(33,33,33),(119,67,40)]
    return colors[num]

def edit_one_image(original_image):
    # Checks for null inputs and edits a single PIL.Image based on inputted modifications

    result=original_image
    
    if mods[0]!=(0,0,0,0): #filter 
        result=filters(result, mods[0])
        
    if mods[1]!=(-1,-1): #logo  
        tmp=[mods[1][0],mods[1][1]]
        if tmp[0]==-1:
            tmp[0]=3
        if tmp[1]==-1:
            tmp[1]=(0,0,0)
        else:
            tmp[1]=convert(tmp[1])
        result=logo(result,tmp[0],tmp[1])
        
    if mods[2]!=(-1,-1,-1,-1,-1): #text 
        tmp=[mods[2][0],mods[2][1],mods[2][2],mods[2][3],mods[2][4]]
        if tmp[2]==-1:
            tmp[2]=1
        if tmp[4]==-1:
            tmp[4]=(0,0,0)
        else:
            tmp[4]=convert(tmp[4])
        result=text(result, tmp[0],tmp[1], tmp[2], tmp[3], tmp[4])
        
    if mods[3]!=(-1,-1,-1): #border
        tmp=[mods[3][0],mods[3][1],mods[3][2]]
        if tmp[0]==-1:
            tmp[0]=0
        if tmp[2]==-1:
            tmp[2]=(0,0,0)
        else:
            tmp[2]=convert(tmp[2])
        result=border(result, tmp[0], tmp[1], tmp[2])
    return result
          
def border(original_image, shape=0, border_width=0.1, color=(0,0,0)):
    """ create a border
            - color (R,G,B)
            - border width (percentage)
            - choose a shape (enter an integer that corresponds with a border option)
    """
    
    # sets border thickness (in pixels) based on given percentage
    width, height = original_image.size
    border_thickness=int(border_width*min(width,height))
    border_image_size=(int(width+2*border_thickness), int(height+2*border_thickness))
    
    result = PIL.Image.new('RGBA', border_image_size, (color[0],color[1],color[2], 255))
    
    # rectangular border w/ inner image rounded=shape 1
    if shape==1:
        im=round_corners(original_image)
        result.paste(im, (border_thickness,border_thickness), mask=im)
        
    # double border=shape 2
    elif shape==2:
        border1_width=int(0.2*border_thickness)
        border1=PIL.Image.new('RGBA', ((width+2*border1_width),(height+2*border1_width)),(color[0],color[1],color[2],255))
        white_border_width=int(0.3*border_thickness)+border1_width
        border_white=PIL.Image.new('RGBA', ((width+2*white_border_width), (height+2*white_border_width)),(255,255,255,0))
        border1.paste(original_image, (border1_width, border1_width))
        border_white.paste(border1, (white_border_width-border1_width, white_border_width-border1_width))
        #return border_white
        x=border_thickness-white_border_width
        result.paste(border_white, (x,x))
        
    # abstract rectangles border = shape 3
    elif shape==3:
        result=random_border(original_image, border_thickness, border_image_size, color)
        
    # simple rectangular border = shape 0
    else:
        result.paste(original_image, (border_thickness,border_thickness))
    return result

def round_corners(original_image):
    '''rounds the corners of the image, radius of rounded corners = 0.05 of minimum
       between the height and width
            - original_image is a PIL image
    '''
    #set the radius of the rounded corners
    width, height = original_image.size
    radius = int(0.05 * min(width, height)) # radius in pixels
    
    rounded_mask = PIL.Image.new('RGBA', (width, height), (127,0,127,0))
    drawing_layer = PIL.ImageDraw.Draw(rounded_mask)
    
    # Overwrite the RGBA values with A=255.
    # The 127 for RGB values was used merely for visualizing the mask
    
    # Draw two rectangles to fill interior with opaqueness
    drawing_layer.polygon([(radius,0),(width-radius,0),
                            (width-radius,height),(radius,height)],
                            fill=(127,0,127,255))
    drawing_layer.polygon([(0,radius),(width,radius),
                            (width,height-radius),(0,height-radius)],
                            fill=(127,0,127,255))

    #Draw four filled circles of opaqueness
    drawing_layer.ellipse((0,0, 2*radius, 2*radius), 
                            fill=(0,127,127,255)) #top left
    drawing_layer.ellipse((width-2*radius, 0, width,2*radius), 
                            fill=(0,127,127,255)) #top right
    drawing_layer.ellipse((0,height-2*radius,  2*radius,height), 
                            fill=(0,127,127,255)) #bottom left
    drawing_layer.ellipse((width-2*radius, height-2*radius, width, height), 
                            fill=(0,127,127,255)) #bottom right
    
    # Make the new image, starting with all transparent
    result = PIL.Image.new('RGBA', original_image.size, (0,0,0,0))
    result.paste(original_image, (0,0), mask=rounded_mask)
    return result 
    
def random_border(original_image, border_thickness, border_image_size, color):
    ''' create an abstract rectangle-based border
            - original_image = PIL image
            - border_thickness is in pixels (integer)
            - border_image_size is a tuple (width, height)
            - color is a tuple (R,G,B)
        
        rectangle height and width is randomly generated
        
        the border appears on a white background, with the widest/tallest(depending 
        on the side of the rectangle being referred to) rectangles equalling 
        border_thickness
    '''
    wid,hei=original_image.size
    
    result = PIL.Image.new('RGBA', border_image_size, (255,255,255,0))
    draw=PIL.ImageDraw.Draw(result)
    
    #make the top part of the border
    topHL=border_thickness
    while topHL<(border_thickness+wid-wid*0.07):
        rhei=random.randint(int(border_thickness*0.2), border_thickness)
        rwid=random.randint(int(wid*0.04), int(wid*0.07))
        draw.rectangle([(topHL,border_thickness-rhei), (topHL+rwid, border_thickness)], color) 
        topHL+=rwid
    rhei=random.randint(int(border_thickness*0.2), border_thickness)
    draw.rectangle([(topHL,border_thickness-rhei), (wid+border_thickness, border_thickness)], color) 
    
    #make the bottom part of the border
    botHL=border_thickness
    while botHL<(border_thickness+wid-wid*0.07):
        rhei=random.randint(int(border_thickness*0.2), border_thickness)
        rwid=random.randint(int(wid*0.04), int(wid*0.07))
        draw.rectangle([(botHL,border_thickness+hei), (botHL+rwid, border_thickness+hei+rhei)], color) 
        botHL+=rwid
    rhei=random.randint(int(border_thickness*0.2), border_thickness)
    draw.rectangle([(botHL,border_thickness+hei), (wid+border_thickness, border_thickness+hei+rhei)], color) 
    
    #make the left part of the border
    leftVL=border_thickness
    while leftVL<(border_thickness+hei-hei*0.07):
        rwid=random.randint(int(border_thickness*0.2), border_thickness)
        rhei=random.randint(int(hei*0.04), int(hei*0.07))
        draw.rectangle([(border_thickness-rwid, leftVL), (border_thickness, leftVL+rhei)], color) 
        leftVL+=rhei
    rwid=random.randint(int(border_thickness*0.2), border_thickness)
    draw.rectangle([(border_thickness-rwid, leftVL), (border_thickness, hei+border_thickness)], color) 
    
    #make the right part of the border
    rightVL=border_thickness
    while rightVL<(border_thickness+hei-hei*0.07):
        rwid=random.randint(int(border_thickness*0.2), border_thickness)
        rhei=random.randint(int(hei*0.04), int(hei*0.07))
        draw.rectangle([(border_thickness+wid, rightVL), (border_thickness+wid+rwid, rightVL+rhei)], color) 
        rightVL+=rhei
    rwid=random.randint(int(border_thickness*0.2), border_thickness)
    draw.rectangle([(border_thickness+wid, rightVL), (border_thickness+wid+rwid, hei+border_thickness)], color) 
    
    #paste the original image on the border result image and return it
    result.paste(original_image, (border_thickness, border_thickness))
    return result
   
                 
def logo(original_image, loc=3, color=(0,0,0)):
    '''this is for adding a logo
            - original_image and logo are PIL images
            - 4 corners = possible locations (loc) corresponding to values 0-3
                --------------
                | 0       2  |
                |            |
                |            |
                |            |
                | 1       3  |
                --------------
                automatic is 3
    '''
    logo = PIL.Image.open('logo image.png')
    wid,hei=original_image.size
    
    colorchange = PIL.Image.new('RGBA', logo.size, (color[0],color[1],color[2],255))
    logo.paste(colorchange, (0,0), logo)
    
    # resize logo based on original image
    rfactor=.1*min(wid,hei)/min(logo.size[0],logo.size[1])
    resized_log= logo.resize((int(rfactor*logo.size[0]), int(rfactor*logo.size[1])))
    
    lwid,lhei=resized_log.size
    dist= int(0.05*min(wid,hei))
    
    # set logo locations
    locations=[(dist,dist),(dist,hei-dist-lhei),(wid-dist-lwid,dist),(wid-dist-lwid,hei-dist-lhei)]
    result = original_image
    result.paste(resized_log, locations[loc], resized_log)
    
    return result
    
def text(original_image, message='HELLO WORLD', size=15, loc=1, fontSelected='arial', fill=(0,0,0)):
    '''add a personalized message, slogan, title, etc.
            - original_image is a PIL image
            - message is a string, automatic is 'HELLO WORLD'
            - size is an integer, automatically 15
            - 4 corners = possible locations (loc) corresponding to values 0-3
                --------------
                | 0       2  |
                |            |
                |            |
                |            |
                | 1       3  |
                --------------
                automatic is 1
            - fontSelected is a string, name of the font, automatically set to arial
            - fill is a tuple for color, (R,G,B), automatically set to black
    '''
    font = PIL.ImageFont.truetype(fontSelected+'.ttf',size)
    wid,hei=original_image.size
    
    result=original_image
    draw=PIL.ImageDraw.Draw(result)
    
    twid, thei = draw.textsize(message, font)
    
    # set text locations
    dist= int(0.02*min(wid,hei))
    locations=[(dist,dist),(dist,hei-dist-thei),(wid-dist-twid,dist),(wid-dist-twid,hei-dist-thei)]
    
    draw.text(locations[loc], message,fill,font) 
    return result
    
def filters(original_image, filterTypes):
    '''apply filters to the image
            - original_image is a PIL image
            - filterTypes is a tuple
    '''
    
    # black and white = filterTypes 1
    img = original_image
    pixels = img.load()
    if 1 in filterTypes:
        for r in range(original_image.size[0]):
            for c in range(original_image.size[1]):
                new = int((0.21*pixels[r,c][0] + 0.71*pixels[r,c][1] + 0.07*pixels[r,c][2]))
                if img.mode == 'RGBA':
                    alpha = pixels[r,c][3]
                    pixels[r,c]=(new,new,new,alpha)
                else:
                    pixels[r,c] = (new, new, new)
    if 2 in filterTypes:
                
    # sepia = filterTypes 2
        for r in range(original_image.size[0]):
            for c in range(original_image.size[1]):
                oRed = int((pixels[r,c][0] * .393) + (pixels[r,c][1] *.769) + (pixels[r,c][2] * .189))
                oGreen = int((pixels[r,c][0] * .349) + (pixels[r,c][1] *.686) + (pixels[r,c][2] * .168))
                oBlue = int((pixels[r,c][0] * .272) + (pixels[r,c][1] *.534) + (pixels[r,c][2] * .131))
                if img.mode == 'RGBA':
                    alpha = pixels[r,c][3]
                    pixels[r,c]=(oRed, oGreen, oBlue, alpha)
                else:
                    pixels[r,c] = (oRed, oGreen, oBlue)
    
    # detail = filterTypes 3
    if 3 in filterTypes:
        img = img.filter(ImageFilter.DETAIL)
        
    # smooth = filterTypes 4
    if 4 in filterTypes:
        img = img.filter(ImageFilter.SMOOTH)

    return img
                                                  
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list


def edit_all_images(directory=None):
    """ Saves a modfied version of each image in directory.
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    # Load all the images
    image_list, file_list = get_images(directory)  

    # Go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        filename, filetype = os.path.splitext(file_list[n])
        
        # Round the corners with default percent of radius
        curr_image = image_list[n]
        new_image = edit_one_image(curr_image) 
        
        # Save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)    
        
        
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
        
    def save_mods(self,index, modifs):
        #placeholder
        mods[index]=modifs
        self.switch_frame(StartPage)
    
    def set_selection(self, one_only):
        change_one_only[0]=one_only
        self.switch_frame(Finalize)

# initialize Home Page and widgets
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
                  
        tk.Label(self).pack()       
        tk.Button(self, text="FINALIZE",
                  command=lambda: master.switch_frame(Select)).pack()
        
# initialize Edit Border screen and widgets
class Border(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        mods[3]=(-1,-1,-1) #border = (shape, border width, color)
        
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
class Filter(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Filter").grid(row = 0, column = 0, columnspan = 4)
        
        mods[0]=(0,0,0,0)
        
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
class Logo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        mods[1]=(-1,-1) #logo = (location, color)

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
class Text(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Text").grid(row = 0, column = 1, columnspan = 2)
        
        mods[2]=(-1,-1,-1,-1,-1) #text = (message, size, location, font, color)
        
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
class Image(tk.Frame):
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
class Select(tk.Frame):
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
class Finalize(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Finalize").grid(row = 0, column = 0) ##
        
        if change_one_only[0]:
            filename = askopenfilename()
            im=PIL.Image.open(filename)
            
            new_image = edit_one_image(im)
            
            new_image_filename = os.path.join(filename + '_edited.png')
            new_image.save(new_image_filename)
            
            wid,hei=new_image.size
            rfactor=500./(max(wid,hei))
            new_image= new_image.resize((int(rfactor*wid), int(rfactor*hei)))
            
            photo=PIL.ImageTk.PhotoImage(new_image)
            imageLabel = tk.Label(self, image=photo)
            imageLabel.grid(row=2, column=0)
            imageLabel.image=photo
            
        else:
            directory = askdirectory()
            edit_all_images(directory)
        
        tk.Button(self, text="Return",
                  command=lambda: master.switch_frame(StartPage)).grid(row = 3, column = 0, columnspan = 4, sticky = "WE")                                                          

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()