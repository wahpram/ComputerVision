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
    newBlank = PIL.Image.new('RGB', (200, 200), (255, 255, 255))
    newBlank = PIL.ImageTk.PhotoImage(newBlank)
    label1 = Label(root, image=newBlank)
    label3 = Label(root, image=newBlank)
    label1.grid(row=1, column=0, sticky= W, pady=2, padx=2)
    label3.grid(row=1, column=1, sticky= W, pady=2, padx=2)


def labelCreate(img, x, y):
    photo = PIL.ImageTk.PhotoImage(img)
    myLabel = Label(image=photo)
    myLabel.image = photo
    myLabel.grid(row=x, column=y, sticky= W, pady=2, padx=2)


def saveFile(path, arrOld, arrNew):
    key = ['x', 'y', 'Red', 'Green', 'Blue']
    key2 = ['input_image', 'new_image']
    arr = []
    
    for (arr1, arr2) in zip(arrOld, arrNew):
        arr.append([arr1, arr2])

    l1 = [dict(zip(key, item)) for item in arrNew]
    l2 = [dict(zip(key2, item)) for item in arr]
    
    with open(f'hasil/Nilai_RGB_{path}.txt', 'w') as f:
        for line in l1:
            f.write(str(line) + '\n')
    
    with open(f'hasil/Nilai_XY_{path}.txt', 'w') as f:
        for line in l2:
            f.write(str(line) + '\n')        
    

def readPixel(img, pathName):
    arr = []
    
    w, h = img.size
    
    for x in range(w):
        for y in range(h):
            redValue = img.getpixel((x, y))[0]
            greenValue = img.getpixel((x,y))[1]
            blueValue = img.getpixel((x, y))[2]
            arr.append([x, y, redValue, greenValue, blueValue])
    
    img.save(f'hasil/{pathName}.jpg')
    
    return arr


def openFile():
    global inputImg
    filePath = tkinter.filedialog.askopenfilename()    
    inputImg = PIL.Image.open(filePath).resize((200, 200))
    inputImg = inputImg.convert('RGB')
    
    labelCreate(inputImg, 1, 0)
    

def newImage():
    global image_arr
    image_arr = []
    
    pathName = 'Input'
    
    image_arr = readPixel(inputImg, pathName)
    
    saveFile(pathName, image_arr, image_arr)


def rotateDeg(x, y, deg):
    rad = radians(deg)
    xh = x * cos(rad) + y * sin(rad)
    yh = -(x * sin(rad)) + y * cos(rad)
    
    return xh, yh


def rotateImage():
    size = inputImg.size
    w = inputImg.width
    h = inputImg.height
    
    userInput = simpledialog.askinteger(title="Input", prompt="Degrees")

    img = PIL.Image.new('RGB', size)
    load = img.load()
    
    for item in image_arr:
        x, y, redValue, greenValue, blueValue = item
        xh, yh = rotateDeg(x - w/2, y - h/2, userInput)
        xh += w/2
        yh += h/2
        
        if 0 <= xh < w and 0 <= yh < h:
            new_r = inputImg.getpixel((int(xh), int(yh)))[0]
            new_g = inputImg.getpixel((int(xh), int(yh)))[1]
            new_b = inputImg.getpixel((int(xh), int(yh)))[2]
            
            load[x, y] = (new_r, new_g, new_b)
    
    labelCreate(img, 1, 1)
    
    pathName = f'Rotate_{userInput}'
    rotateArr = readPixel(img, pathName)
    
    saveFile(pathName, image_arr, rotateArr)


def button(root, text, command, x, y):
    buttonH = 1
    buttonW = 28
    button = Button(root, text=text, command=command, height=buttonH, width=buttonW)
    button.grid(row=x, column=y, sticky= W, pady=2, padx=2)


def flipImage(v):
    size = inputImg.size
    w = inputImg.width
    h = inputImg.height
    
    img = PIL.Image.new('RGB', size)
    load = img.load()
    
    for item in image_arr:
        x, y, redValue, greenValue, blueValue = item
        
        match v:
            case 1:
                xh = w - 1 - x
                yh = y
                pathName = 'Flip_Horizontal'
            case 2:
                xh = x
                yh = h - 1 - y
                pathName = 'Flip_Vertical'
            case 3:
                xh = w - 1 - x
                yh = h - 1 - y
                pathName = 'Flip_Both'
            
        load[xh, yh] = (redValue, greenValue, blueValue)
                
    labelCreate(img, 1, 1)
    
    flipArr = readPixel(img, pathName)
    saveFile(pathName, image_arr, flipArr)


def button2(root, text, x, y, v, command):
    buttonH = 1
    buttonW = 28
    radiobutton = Button(root, text=text, height=buttonH, width=buttonW, command= lambda: command(v))
    radiobutton.grid(row=x, column=y, sticky= '', pady=2, padx=2)


def text(root, text, row, column):
    Label(root, text=text).grid(row=row, column=column, sticky= '', pady=2, padx=2)
    

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
    # root.geometry("814x620")
    
    window(root)
    
    text(root, 'IMAGE INPUT', 0, 0)
    text(root, 'IMAGE OUTPUT', 0, 1)
    
    button(root, 'OPEN FILE', openFile, 2, 0)
    button(root, 'READ IMAGE', newImage, 3, 0)
    button(root, 'ROTATE IMAGE', rotateImage, 2, 1)
    
    button2(root, 'FLIP HORIZONTAL', 3, 1, 1, flipImage)
    button2(root, 'FLIP VERTICAL', 4, 1, 2, flipImage)
    button2(root, 'FLIP BOTH', 5, 1, 3, flipImage)
    
    button2(root, 'EXIT', 4, 0, root, exit)
    
    root.mainloop()


if __name__ == "__main__":
    main()
