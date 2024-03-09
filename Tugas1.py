import PIL.Image
import tkinter.filedialog
import os
from math import *
from tkinter import *
from array import *
from PIL import ImageTk
from pathlib import Path
from tkinter import simpledialog


def window(root):
    newBlank = PIL.Image.new('RGB', (204, 204), (255, 255, 255))
    newBlank = PIL.ImageTk.PhotoImage(newBlank)
    label1 = Label(root, image=newBlank)
    # label2 = Label(root, image=newBlank)
    label3 = Label(root, image=newBlank)
    label1.place(x=150, y=100)
    # label2.place(x=300, y=100)
    label3.place(x=400, y=100)


def labelCreate(img, x, y):
    newSize = img.resize((204, 204))
    photo = PIL.ImageTk.PhotoImage(newSize)
    myLabel = Label(image=photo)
    myLabel.image = photo
    myLabel.place(x=x, y=y)
    
    return newSize


def readPixel(img, pathName): 
    global w, h 
    arr = []
    l = []
    key = ['x', 'y', 'Red', 'Green', 'Blue']
    
    w, h = img.size
    
    for x in range(w):
        for y in range(h):
            redValue = img.getpixel((x, y))[0]
            greenValue = img.getpixel((x,y))[1]
            blueValue = img.getpixel((x, y))[2]
            arr.append([x, y, redValue, greenValue, blueValue])
    
    for item in arr:        
        d1 = dict(zip(key, item))
        l.append(d1)
        
    with open(f'hasil/{pathName}.txt', 'w') as f:
        for line in l:
            f.write("%s\n" % line)
    
    img.save(f'hasil/{pathName}.jpg')
    
    return arr


def openFile():
    global resizedImg
    filePath = tkinter.filedialog.askopenfilename()    
    img = PIL.Image.open(filePath)
    img = img.convert('RGB')
    
    resizedImg = labelCreate(img, 150, 100)
    

def newImage():
    global image_arr
    image_arr = []
    
    pathName = 'Nilai_RGB'
    image_arr = readPixel(resizedImg, pathName)


def rotateDeg(x, y, deg):
    rad = radians(deg)
    xh = x * cos(rad) + y * sin(rad)
    yh = -(x * sin(rad)) + y * cos(rad)
    
    return xh, yh


def rotateImage():
    size = w, h
    
    userInput = simpledialog.askinteger(title="Input", prompt="Degrees")

    img = PIL.Image.new('RGB', size)
    
    for item in image_arr:
        x, y, redValue, greenValue, blueValue = item
        xh, yh = rotateDeg(x - w/2, y - h/2, userInput)
        xh += w/2
        yh += h/2
        
        if 0 <= xh < w and 0 <= yh < h:
            img.putpixel((x, y), resizedImg.getpixel((int(xh), int(yh))))
    
    labelCreate(img, 400, 100)
    
    pathName = f'Nilai_RGB_Rotate_{userInput}'
    readPixel(img, pathName)


def button(root, text, command, x, y):
    buttonH = 1
    buttonW = 28
    button = Button(root, text=text, command=command, height=buttonH, width=buttonW)
    button.place(x= x, y= y)


def flipImage(v):
    size = w, h 
    
    img = PIL.Image.new('RGB', size)
    load = img.load()
    
    for item in image_arr:
        x, y, redValue, greenValue, blueValue = item
        
        match v:
            case 1:
                xh = w - 1 - x
                yh = y
                pathName = 'Nilai_RGB_Flip_Horizontal'
            case 2:
                xh = x
                yh = h - 1 - y
                pathName = 'Nilai_RGB_Flip_Vertical'
            case 3:
                xh = w - 1 - x
                yh = h - 1 - y
                pathName = 'Nilai_RGB_Flip_Both'
            
        load[xh, yh] = (redValue, greenValue, blueValue)
                
    labelCreate(img, 400, 100)
    
    readPixel(img, pathName)


def flipButton(root, text, x, y, v, command):
    buttonH = 1
    buttonW = 28
    radiobutton = Button(root, text=text, height=buttonH, width=buttonW, command= lambda: command(v))
    radiobutton.place(x=x, y=y)


def text(root, text, x, y):
    l = Label(root, text=text).place(x=x, y=y)
    

def exit(root):
    folder = 'hasil/'
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        try:
            os.remove(filepath)
            print(f'{filepath} deleted!')
        except Exception as e:
            print(f'Delete failed, because {e}')
            
    root.destroy()
    
    
def main():
    root = Tk()
    root.title("Read Pixel Value of Image")
    root.configure(background='#242424')
    root.geometry("814x620")
    
    window(root)
    
    text(root, 'IMAGE INPUT', 215, 80)
    text(root, 'IMAGE OUTPUT', 455, 80)
    
    button(root, 'OPEN FILE', openFile, 150, 320)
    button(root, 'READ IMAGE', newImage, 150, 350)
    button(root, 'ROTATE IMAGE', rotateImage, 400, 410)
    
    flipButton(root, 'FLIP HORIZONTAL', 400, 320, 1, flipImage)
    flipButton(root, 'FLIP VERTICAL', 400, 350, 2, flipImage)
    flipButton(root, 'FLIP BOTH', 400, 380, 3, flipImage)
    
    flipButton(root, 'EXIT', 400, 440, root, exit)
    
    root.mainloop()


if __name__ == "__main__":
    main()
