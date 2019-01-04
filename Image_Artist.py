import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw            
import random
import PIL.ImageFont  

def edit_one_image(original_image,border_width=0.1, color=(0,0,0)):
    """ Edit a PIL.Image, the following code is a placeholder
    
        we need to decide the order of the edits i guess, im thinking filter first,
        then logo, text, border?
        
        rounding corners might affect text and logos we put in the corner, will need to check on that
        
    """
    
    width, height = original_image.size
    border_thickness=border_width*min(width,height)
    border_image_size=(width+2*border_thickness, height+2*border_thickness)
    
    result = PIL.Image.new('RGBA', border_image_size, (color[0],color[1],color[2], 255))
    result.paste(original_image, (border_thickness,border_thickness))
    return result
          
def border(original_image, shape=0, border_width=0.1, color=(0,0,0)):
    """ create a borderD:\Student Work\Adrienne Yu\cse1819\1.4.5 Source Files\1.4.5 Images
            - color (R,G,B)D:\Student Work\Adrienne Yu\cse1819\1.4.5 Source Files\1.4.5 Images
            - border width (percentage)
            - choose a shape (enter an integer that corresponds with a border option)
    """
    
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
        border_white=PIL.Image.new('RGBA', ((width+2*white_border_width), (height+2*white_border_width)),(255,255,255,255))
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
    
    result = PIL.Image.new('RGBA', border_image_size, (255,255,255,255))
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
          
def logo(original_image, logo, loc=3):
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
    wid,hei=original_image.size
    
    rfactor=.1*min(wid,hei)/min(logo.size[0],logo.size[1])
    resized_log= logo.resize((int(rfactor*logo.size[0]), int(rfactor*logo.size[1])))
    
    lwid,lhei=resized_log.size
    dist= int(0.05*min(wid,hei))
    
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
    dist= int(0.02*min(wid,hei))
    locations=[(dist,dist),(dist,hei-dist-thei),(wid-dist-twid,dist),(wid-dist-twid,hei-dist-thei)]
    
    draw.text(locations[loc], message,fill,font) 
    return result
    
def filter(original_image, type):
    '''apply filters to the image
            - original_image is a PIL image
            - type could be a string or a list or something, but currently up glowing green --> should probs change name
    '''
    # black and white = type 1
    img = original_image
    pixels = img.load()
    if 1 in type:
        for r in range(original_image.size[0]):
            for c in range(original_image.size[1]):
                new = int((0.21*pixels[r,c][0] + 0.71*pixels[r,c][1] + 0.07*pixels[r,c][2]))
                alpha = pixels[r,c][3]
                pixels[r,c] = (new, new, new, alpha)
                
    # sepia
    if 2 in type:
        for r in range(original_image.size[0]):
            for c in range(origina66l_image.size[1]):
                iRed = pixels[r,c][0]
                iGreen = pixels[r,c][2]
                iBlue = pixels[r,c][2]
                oRed = int((pixels[r,c][0] * .393) + (pixels[r,c][1] *.769) + (pixels[r,c][2] * .189))
                oGreen = int((pixels[r,c][0] * .349) + (pixels[r,c][1] *.686) + (pixels[r,c][2] * .168))
                oBlue = int((pixels[r,c][0] * .272) + (pixels[r,c][1] *.534) + (pixels[r,c][2] * .131))
                alpha = pixels[r,c][3]
                pixels[r,c] = (oRed, oGreen, oBlue, alpha)
    
    # detail = type 3
    if 3 in type:
        img = img.filter(ImageFilter.DETAIL)
        
    # smooth = type 4
    if 4 in type:
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


def edit_all_images(directory=None, ):
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
        print n
        filename, filetype = os.path.splitext(file_list[n])
        
        # Round the corners with default percent of radius
        curr_image = image_list[n]
        new_image = edit_one_image(curr_image) 
        
        # Save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)    
        
    