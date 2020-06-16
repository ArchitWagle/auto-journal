import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import pickle

fn = '/home/archit/Downloads/alphabet.jpg'

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

img = []
img_bakcup = []
char_dict = dict()
def BnW():
    # automatic thresholding to BW
    im_gray = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    #resize image to 50%
    new_width = int(40*im_bw.shape[1]/ 100)
    new_height = int(40*im_bw.shape[0]/ 100)
    im_bw = cv2.resize(im_bw, (new_width, new_height))
    
    line_thickness = 2
    cv2.line(im_bw, (int(new_width/3), 0), (int(new_width/3), new_height), (0, 255, 0), thickness=line_thickness)
    cv2.line(im_bw, (int(2*new_width/3), 0), (int(2*new_width/3), new_height), (0, 255, 0), thickness=line_thickness)    
        
    #cv2.imshow('image',im_bw)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows() 


    return im_bw

ix = -1
iy = -1
rect = [0,0]
rect_list = []
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
    
   
def interface(src):
    global img, img_bakcup
    img = src.copy()
    img_bakcup = src.copy()
    cv2.imshow('image',src)
    cv2.setMouseCallback('image', draw_drag_rectangle)
    
    
    while True:

        cv2.imshow('image', img)
        if cv2.waitKey(10) == 27:
            break
        
    
    cv2.destroyAllWindows()
    
    for i in range(len(rect_list)):
        temp = rect_list[i]
        char_dict[i]= img_bakcup[temp[0][1]:temp[1][1],temp[0][0]:temp[1][0]]
        print(temp,char_dict[i],)
        while True:
            cv2.imshow('x', char_dict[i])
            if cv2.waitKey(100) == 27:
                break
    cv2.destroyAllWindows()
    save_obj(char_dict, "handwriting_dict" )
        
        
    
def hello():
    im_bw = BnW()
    interface(im_bw)



hello()
