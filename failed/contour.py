import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pickle

fn = 'images/sample.jpeg'

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

img = []
img_bakcup = []
char_dict = dict()
ix = -1
iy = -1
rect = [0,0]
rect_list = []

def BnW():
    # automatic thresholding to BW
    im_gray = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 150, 255, cv2.THRESH_BINARY)
    #im_bw =cv2.adaptiveThreshold(im_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

    #resize image to 50%
    new_width = int(60*im_bw.shape[1]/ 100)
    new_height = int(60*im_bw.shape[0]/ 100)
    im_bw = cv2.resize(im_bw, (new_width, new_height))

    return im_bw


def draw_drag_rectangle(event, x, y, flags, param):

    global img,ix,iy,rect,rect_list,img_bakcup
    drawing = False
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y

    if event == cv2.EVENT_RBUTTONDOWN:
        rect_list.append(rect)
        for x in rect_list:
            cv2.rectangle(img, pt1=x[0], pt2=x[1],color=(0,255,255),thickness=2)
        print(rect_list)
        

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img2 = img_bakcup.copy()
            cv2.rectangle(img2, pt1=(ix,iy), pt2=(x, y),color=(0,255,255),thickness=2)
            img = img2
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        img2 = img_bakcup.copy()
        cv2.rectangle(img2, pt1=(ix,iy), pt2=(x, y),color=(0,255,255),thickness=2)
        rect = ((ix,iy),(x, y))
        img = img2
    
   
def manual_interface():
    global img, img_bakcup
    cv2.imshow('image',img)
    cv2.setMouseCallback('image', draw_drag_rectangle)
       
    while True:
        cv2.imshow('image', img)
        if cv2.waitKey(10) == 27:
            break
    cv2.destroyAllWindows()
    
    for i in range(len(rect_list)):
        temp = rect_list[i]
        char_dict[i]= img_bakcup[temp[0][1]:temp[1][1],temp[0][0]:temp[1][0]]
        while True:
            cv2.imshow('x', char_dict[i])
            if cv2.waitKey(100) == 27:
                break
    cv2.destroyAllWindows()
    save_obj(char_dict, "handwriting_dict1" )
    

alpha_dict = dict()
punctuation_dict = dict()
number_dict = dict()




def draw_classifying_rect(event, x, y, flags, param):
    global img,ix,iy,rect,rect_list,img_bakcup
    drawing = False
    font = cv2.FONT_HERSHEY_SIMPLEX
    captions = ["alphabets","special symbols","numbers"]
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y

    if event == cv2.EVENT_RBUTTONDOWN:
        rect_list.append(rect)
        for x in rect_list:
            cv2.rectangle(img, pt1=x[0], pt2=x[1],color=(0,255,255),thickness=2)
            cv2.putText(img,captions[rect_list.index(x)],x[0], font, 1,(0,255,255),2,cv2.LINE_AA)
        

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img2 = img_bakcup.copy()
            cv2.rectangle(img2, pt1=(ix,iy), pt2=(x, y),color=(0,255,255),thickness=2)
            img = img2
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        img2 = img_bakcup.copy()
        cv2.rectangle(img2, pt1=(ix,iy), pt2=(x, y),color=(0,255,255),thickness=2)
        rect = ((ix,iy),(x, y))
        img = img2
        
            
    
def auto_interface():
    global img, img_bakcup, rect_list
    cv2.imshow('image',img)
    cv2.setMouseCallback('image', draw_classifying_rect)     
    rect_list = []
    while True:
        cv2.imshow('image', img)
        if cv2.waitKey(10) == 27:
            break
    cv2.destroyAllWindows()

    
    
def mssg_box():
    MsgBox = tk.messagebox.askquestion ('Manual/Automatic Handwriting Recognition','Do you want to manually segment your handwriting?',icon = 'warning')
    if MsgBox == 'yes':
        manual_interface()
    else:
        tk.messagebox.showinfo('Return','We will automatically segment the image')
        auto_interface()
        

def manual_automatic(im_bw):
    global img, img_bakcup
    root= tk.Tk()
    canvas1 = tk.Canvas(root, width = 300, height = 300)
    canvas1.pack()
    button1 = tk.Button (root, text='Select Auto or Manual Handwriting recognition',command=mssg_box,bg='brown',fg='white')
    canvas1.create_window(150, 150, window=button1)
    root.mainloop()
    
    
        
    
def hello():
    global img, img_bakcup
    im_bw = BnW()
    img = im_bw.copy()
    img_bakcup = im_bw.copy()
    manual_automatic(im_bw)



hello()
