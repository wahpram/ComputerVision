import PIL.Image
import tkinter.filedialog
from PIL import ImageTk
from tkinter import *
from array import *
from pathlib import Path
from tkinter import simpledialog

global arr, w, h

def labels(root):
    newBlank = PIL.Image.new('RGB', (204, 204), (255, 255, 255))
    newBlank = PIL.ImageTk.PhotoImage(newBlank)
    
    label1 = Label(root, image=newBlank)
    label2 = Label(root, image=newBlank)
    label3 = Label(root, image=newBlank)
    label1.place(x=50, y=100)
    label2.place(x=300, y=100)
    label3.place(x=550, y=100)
    

def readPixel(): 
    global w, h, arr, l   
    
    x = 0
    y = 0
    arr = []
    l = []
    
    filePath = tkinter.filedialog.askopenfilename()    
    fileName = Path(filePath).stem
    img = PIL.Image.open(filePath)
    img = img.convert('RGB')
    newSize = img.resize((204, 204))
    
    photo = PIL.ImageTk.PhotoImage(newSize)
    myLabel = Label(image=photo)
    myLabel.image = photo
    myLabel.place(x= 50, y= 100)
    
    w, h = img.size
    
    for i in range(w):
        x = i
        y = 0
        
        for j in range(h):
            y = j
            redValue = img.getpixel((x, y))[0]
            greenValue = img.getpixel((x,y))[1]
            blueValue = img.getpixel((x, y))[2]
            arr.append([x, y, redValue, greenValue, blueValue])
    
    for item in arr:
        key = ['x', 'y', 'Red', 'Green', 'Blue']
        
        d1 = zip(key, item)
        l.append(dict(d1))
        
    with open('hasil/value.txt', 'w') as f:
        for line in l:
            f.write("%s\n" % line)
    
    
def newImage():
    x = 0
    y = 0
    size = w, h
    
    img = PIL.Image.new('RGB', size)
    load = img.load()
    
    for item in arr:
        x, y, redValue, greenValue, blueValue = item
        load[x, y] = (redValue, greenValue, blueValue)
    
    newSize = img.resize((204, 204))
    photo = PIL.ImageTk.PhotoImage(newSize)
    myLabel = Label(image=photo)
    myLabel.image = photo
    myLabel.place(x=300, y=100) 


def rotateImage():
    size = w, h
    
    # userInput = simpledialog.askinteger(title="Input", prompt="Degrees")

    img = PIL.Image.new('RGB', size)
    load = img.load()
    
    wh = h
    hh = w
    for item in arr:
        x, y, redValue, greenValue, blueValue = item
        xh = wh - 1 - y
        yh = x
        load[xh, yh] = (redValue, greenValue, blueValue)
    
    newSize = img.resize((204, 204))
    photo = PIL.ImageTk.PhotoImage(newSize)
    myLabel = Label(image=photo)
    myLabel.image = photo
    myLabel.place(x=550, y=100)


def flipImage(v):
    size = w, h 
    
    img = PIL.Image.new('RGB', size)
    load = img.load()
    
    match v:
        case 1:
            for item in arr:
                x, y, redValue, greenValue, blueValue = item
                xh = w - 1 - x
                yh = y
                load[xh, yh] = (redValue, greenValue, blueValue)
        case 2:
            for item in arr:
                x, y, redValue, greenValue, blueValue = item
                xh = x
                yh = h - 1 - y
                load[xh, yh] = (redValue, greenValue, blueValue)
        case 3:
            for item in arr:
                x, y, redValue, greenValue, blueValue = item
                xh = w - 1 - x
                yh = h - 1 - y
                load[xh, yh] = (redValue, greenValue, blueValue)
                
    newSize = img.resize((204, 204))
    photo = PIL.ImageTk.PhotoImage(newSize)
    myLabel = Label(image=photo)
    myLabel.image = photo
    myLabel.place(x=550, y=100)
    
def button(root):
    imH = 1
    imW = 28
    
    openButton = Button(root, text='OPEN FILE', command=readPixel, height=imH, width=imW)
    openButton.place(x= 50, y= 320)
    
    readButton = Button(root, text='READ IMAGE', command=newImage, height=imH, width=imW)
    readButton.place(x= 300, y= 320)
    
    rotateButton = Button(root, text='ROTATE', command=rotateImage, height=imH, width=imW)
    rotateButton.place(x=550, y=320)
    
    flipHorizontal = Button(root, text='FLIP HORIZONTAL', command= lambda: flipImage(1), height=imH, width=imW)
    flipHorizontal.place(x=550, y= 350)
    
    flipVertical = Button(root, text='FLIP VERTIKAL', command= lambda: flipImage(2), height=imH, width=imW)
    flipVertical.place(x=550, y= 380)
    
    flipComb = Button(root, text='FLIP BOTH', command= lambda: flipImage(3), height=imH, width=imW)
    flipComb.place(x=550, y= 410)
    
def main():
    root = Tk()
    root.title("Read Pixel Value of Image")
    root.configure(background='#242424')
    root.geometry("814x620")
    
    labels(root)
    button(root)
    
    
    root.mainloop()

if __name__ == "__main__":
    main()