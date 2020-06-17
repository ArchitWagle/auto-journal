import cv2
import numpy as np
import pickle

def nothing(x):
    pass

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


fn = 'images/sample.jpeg'
imgray = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)

cv2.namedWindow('image')

# create trackbars for threshold change
cv2.createTrackbar('T','image',0,255,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

def is_pixel_row_white(x,T):
    for i in x:
        if i<T:
            return False
    return True
   
def is_pixel_column_white(x,T):
    for i in x:
        if i[0]<T:
            return False
    return True



def process_characters(x, i, T, img_crop):
    
    # remove space from top and below 
    
    y_top = 0
    while  y_top<len(img_crop):
        if is_pixel_row_white(img_crop[y_top],T):
            y_top+=1
        else:
            break
    
    y_bottom = len(img_crop)-1
    while y_bottom >0:
        if is_pixel_row_white(img_crop[y_bottom],T):
            y_bottom-=1
        else:
            break        
        
    img_crop = img_crop[y_top:y_bottom, 0:img_crop.shape[1]]
    return img_crop

def apply_segmentation(img,T, save):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # types of characters available, along with their numbers
    char_types = {'alphabet':26,'punctuation':16,'number':9}
    captions = ['alphabet','punctuation','number']
    
    img_backup = img.copy()
    
    # This will store the Y coordinates of the bounding rectangles for the 
    # character classes defined above, The X coordinates are the same as the 
    # window size
    character_class_BR = [[0,0] for i in char_types]
    
    if save:
        storage_dict = [dict() for i in char_types]
    
    # while scanning through the rows, this variable will act as a flag as to 
    # when one class end and the other begins
    active = False
    count = 0
    
    # scan the image row wise to separate the samples for alphabets and numbers 
    for i in range(len(img)):
        row = img[i]  
        if(count == len(captions)):
            break
        # currently scanning a line containing a character
        if active:
            if is_pixel_row_white(row,T):
                character_class_BR[count][1] = i
                count += 1
                active = False
            else:
                pass
                
        # currently scanning a line not containing any character
        else:
            if is_pixel_row_white(row,T):
                pass
            else:
                character_class_BR[count][0] = i   
                active = True
    
    # display boxes in image             
    for x in character_class_BR:
        cv2.rectangle(img, pt1=(0,x[0]), pt2=(img.shape[1],x[1]),color=(0,255,255),thickness=2)    
        cv2.putText(img,captions[character_class_BR.index(x)],(0,x[0]), font, 1,(0,255,255),2,cv2.LINE_AA)
    
    # iterate over all character classes to segment them separately
    for x in range(len(character_class_BR)):
        
        # The total number of characters in class indexed x
        char_max = char_types[captions[x]]
        
        ans = [] 
        # X coords of Bounding Rect of character class indexed x
        bounds_X = character_class_BR[x]
        active = False
        count = 0
        
        for i in range(img.shape[1]):
            
            if(count == char_max):
                break
            
            column = img_backup[bounds_X[0]:bounds_X[1],i:i+1]
            
            if active:
                if is_pixel_column_white(column,T):
                    ans[count][1] = [bounds_X[1],i]
                    count+=1
                    active = False
                else:
                    pass
            else:
                if is_pixel_column_white(column,T):
                    pass
                else:
                    ans.append([[bounds_X[0],i],[0,0]])
                    active = True
        
        for i in range(len(ans)):
            temp = ans[i]
            cv2.rectangle(img, pt1=(temp[0][1],temp[0][0]), pt2=(temp[1][1],temp[1][0]),color=(0,255,255),thickness=1)         
            
            if save :           
                
                storage_dict[x][i]=  process_characters(x, i , T,img_backup[temp[0][1]:temp[1][1]+1,temp[0][0]:temp[1][0]+1])
            
    if save:
        save_obj(storage_dict,"storage_dict")
        return
    return img

t = -1
s = -1
while(1):
    t = cv2.getTrackbarPos('T','image')
    s = cv2.getTrackbarPos(switch,'image')
    
    (thresh, img) = cv2.threshold(imgray, t, 255, cv2.THRESH_BINARY)
    
    if(s==1): 
        img1 = apply_segmentation(img,t, False)
        cv2.imshow('image',img1)
    else:
        cv2.imshow('image',img)
        
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
if(s==1):
    apply_segmentation(img,t, True)
cv2.destroyAllWindows()

