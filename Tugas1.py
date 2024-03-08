import PIL.Image
import tkinter.filedialog
from PIL import ImageTk
from math import *
from tkinter import *
from array import *
from pathlib import Path
from tkinter import simpledialog


def window(root):
    newBlank = PIL.Image.new('RGB', (204, 204), (255, 255, 255))
    newBlank = PIL.ImageTk.PhotoImage(newBlank)
    label1 = Label(root, image=newBlank)
    label2 = Label(root, image=newBlank)
    label3 = Label(root, image=newBlank)
    label1.place(x=50, y=100)
    label2.place(x=300, y=100)
    label3.place(x=550, y=100)


def labelCreate(img, x, y):
    newSize = img.resize((204, 204))
    photo = PIL.ImageTk.PhotoImage(newSize)
    myLabel = Label(image=photo)
    myLabel.image = photo
    myLabel.place(x=x, y=y)
    
    return newSize


def readPixel(): 
    global w, h, arr   
    arr = []
    l = []
    key = ['x', 'y', 'Red', 'Green', 'Blue']
    
    filePath = tkinter.filedialog.askopenfilename()    
    fileName = Path(filePath).stem
    img = PIL.Image.open(filePath)
    img = img.convert('RGB')
    
    resizedImg = labelCreate(img, 50, 100)
    
    w, h = resizedImg.size
    
    for x in range(w):
        for y in range(h):
            redValue = resizedImg.getpixel((x, y))[0]
            greenValue = resizedImg.getpixel((x,y))[1]
            blueValue = resizedImg.getpixel((x, y))[2]
            arr.append([x, y, redValue, greenValue, blueValue])
    
    for item in arr:        
        d1 = dict(zip(key, item))
        l.append(d1)
        
    with open('hasil/value.txt', 'w') as f:
        for line in l:
            f.write("%s\n" % line)


def newImage():
    global copyImg
    size = w, h
    
    copyImg = PIL.Image.new('RGB', size)
    load = copyImg.load()
    
    for item in arr:
        x, y, redValue, greenValue, blueValue = item
        load[x, y] = (redValue, greenValue, blueValue)
    
    labelCreate(copyImg, 300, 100)


def rotateDeg(x, y, deg):
    rad = radians(deg)
    xh = x * cos(rad) - y * sin(rad)
    yh = x * sin(rad) + y * cos(rad)
    
    return xh, yh


def rotateImage():
    size = w, h
    
    userInput = simpledialog.askinteger(title="Input", prompt="Degrees")

    img = PIL.Image.new('RGB', size)
    
    for item in arr:
        x, y, redValue, greenValue, blueValue = item
        xh, yh = rotateDeg(x - w/2, y - h/2, userInput)
        xh += w/2
        yh += h/2
        
        if 0 <= xh < w and 0 <= yh < h:
            img.putpixel((x, y), copyImg.getpixel((int(xh), int(yh))))
    
    labelCreate(img, 550, 100)


def button(root, text, command, x, y):
    buttonH = 1
    buttonW = 28
    button = Button(root, text=text, command=command, height=buttonH, width=buttonW)
    button.place(x= x, y= y)


def flipImage(v):
    size = w, h 
    
    img = PIL.Image.new('RGB', size)
    load = img.load()
    
    for item in arr:
        x, y, redValue, greenValue, blueValue = item
        
        match v:
            case 1:
                xh = w - 1 - x
                yh = y
            case 2:
                xh = x
                yh = h - 1 - y
            case 3:
                xh = w - 1 - x
                yh = h - 1 - y
            
        load[xh, yh] = (redValue, greenValue, blueValue)
                
    labelCreate(img, 550, 100)


def flipButton(root, text, x, y, v):
    buttonH = 1
    buttonW = 28
    radiobutton = Button(root, text=f'FLIP {text}', height=buttonH, width=buttonW, command= lambda: flipImage(v))
    radiobutton.place(x=x, y=y)
  
    
def main():
    root = Tk()
    root.title("Read Pixel Value of Image")
    root.configure(background='#242424')
    root.geometry("814x620")
    
    window(root)
    
    button(root, 'OPEN FILE', readPixel, 50, 320)
    button(root, 'READ IMAGE', newImage, 300, 320)
    button(root, 'ROTATE IMAGE', rotateImage, 550, 410)
    
    flipButton(root, 'HORIZONTAL', 550, 320, 1)
    flipButton(root, 'VERTICAL', 550, 350, 2)
    flipButton(root, 'BOTH', 550, 380, 3)
    
    root.mainloop()


if __name__ == "__main__":
    main()
