import PIL.Image
import tkinter.filedialog
import os
from math import *
from tkinter import *
from array import *
from PIL import ImageTk
from pathlib import Path
from tkinter import simpledialog
from tkinter import messagebox


def create_window(root):
    newBlank = PIL.Image.new('RGB', (300, 300), (255, 255, 255))
    newBlank = PIL.ImageTk.PhotoImage(newBlank)
    label1 = Label(root, image=newBlank)
    label3 = Label(root, image=newBlank)
    label1.grid(row=1, column=0, sticky= W, pady=10, padx=2)
    label3.grid(row=1, column=1, sticky= W, pady=10, padx=2)


def create_widgets(img, x, y):
    photo = PIL.ImageTk.PhotoImage(img)
    myLabel = Label(image=photo)
    myLabel.image = photo
    myLabel.grid(row=x, column=y, sticky= W, pady=2, padx=2)


def create_button(root, text, command, x, y):
    buttonH = 1
    buttonW = 42
    Button(root, text=text, command=command, height=buttonH, width=buttonW).grid(row=x, column=y, sticky= '', padx=2)


def create_button2(root, text, x, y, v, command):
    buttonH = 1
    buttonW = 42
    Button(root, text=text, height=buttonH, width=buttonW, command= lambda: command(v)).grid(row=x, column=y, sticky= '', padx=2)


def create_text(root, text, row, column):
    Label(root, text=text, width=42, height=2).grid(row=row, column=column, sticky= '', pady=2, padx=2)


def msbox():
    messagebox.showerror('error', 'Make sure input image first')
    print(f'Input image is not defined')


def save_file(path, arrOld, arrNew):
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
    

def read_pixel_value(img, pathName):
    global arr
    arr = []
    
    w, h = img.size
    
    for x in range(w):
        for y in range(h):
            rgb_value = img.getpixel((x, y))
            arr.append([x, y, *rgb_value])
    
    img.save(f'hasil/{pathName}.jpg')
    
    return arr


def open_file():
    global inputImg
    
    try:
        filePath = tkinter.filedialog.askopenfilename()    
        inputImg = PIL.Image.open(filePath).resize((300, 300))
        inputImg = inputImg.convert('RGB')
    
        create_widgets(inputImg, 1, 0)
    except:
        return

def read_image():
    global image_arr
    
    try:
        image_arr = []
        
        pathName = 'Input'
        
        image_arr = read_pixel_value(inputImg, pathName)
        
        save_file(pathName, image_arr, image_arr)
    
    except NameError:
        msbox()


def rotate_image2(v):
    try:
        size = inputImg.size
        w = inputImg.width
        h = inputImg.height
        
        img = PIL.Image.new('RGB', size)
        load = img.load()
        
        for item in image_arr:
            x, y, redValue, greenValue, blueValue = item
            
            match v:
                case 1:
                    wn = h
                    hn = w
                    xn = wn - 1 - y
                    yn = x
                    pathName = f'Rotate_90°'
                case 2:
                    xn = w - 1 - x
                    yn = h - 1 - y
                    pathName = f'Rotate_180°'
            
            load[xn, yn] = (redValue, greenValue, blueValue)
            
        create_widgets(img, 1, 1)
        rotateArr = read_pixel_value(img, pathName)
        save_file(pathName, image_arr, rotateArr)
    
    except:
        msbox()
    

def flip_image(v):
    try:
        size = inputImg.size
        w = inputImg.width
        h = inputImg.height
        
        img = PIL.Image.new('RGB', size)
        load = img.load()
        
        for item in image_arr:
            x, y, redValue, greenValue, blueValue = item
            
            match v:
                case 1:
                    xn = w - 1 - x
                    yn = y
                    pathName = 'Flip_Horizontal'
                case 2:
                    xn = x
                    yn = h - 1 - y
                    pathName = 'Flip_Vertical'
                case 3:
                    xn = w - 1 - x
                    yn = h - 1 - y
                    pathName = 'Flip_Both'
                
            load[xn, yn] = (redValue, greenValue, blueValue)
                    
        create_widgets(img, 1, 1)
        flipArr = read_pixel_value(img, pathName)
        save_file(pathName, image_arr, flipArr)
    
    except:
        msbox()


def exit(root):
    folder = 'hasil/'
    
    res = messagebox.askquestion('exit', 'Are you sure?')
    
    if res == 'yes':
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            try:
                os.remove(filepath)
                print(f'{filepath} deleted!')
            except Exception as e:
                print(f'Delete failed, because {e}')
            
        root.destroy()
    else:
        messagebox.showinfo('return', 'Returning to app')
    

def main():
    root = Tk()
    root.title("Read Pixel Value of Image")
    root.configure(background='#242424')
    
    create_window(root)
    
    create_text(root, 'IMAGE INPUT', 0, 0)
    create_text(root, 'IMAGE OUTPUT', 0, 1)
    
    create_button(root, 'OPEN FILE', open_file, 2, 0)
    create_button(root, 'READ IMAGE', read_image, 3, 0)
    
    create_button2(root, 'ROTATE IMAGE 90°', 2, 1, 1, rotate_image2)
    create_button2(root, 'ROTATE IMAGE 180°', 3, 1, 2, rotate_image2)
    create_button2(root, 'FLIP HORIZONTAL', 4, 1, 1, flip_image)
    create_button2(root, 'FLIP VERTICAL', 5, 1, 2, flip_image)
    create_button2(root, 'FLIP VERTICAL & HORIZONTAL', 6, 1, 3, flip_image)
    
    create_button2(root, 'EXIT', 4, 0, root, exit)
    
    root.mainloop()


if __name__ == "__main__":
    main()