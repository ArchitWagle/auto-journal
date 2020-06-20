import cv2
import numpy as np
import pickle

def nothing(x):
    pass

# function to save the character images
def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


# read the sample file
storage_dict = []
fn = 'images/sample_r.jpeg'
imgray = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)
cv2.namedWindow('image')

# create trackbars for threshold change
cv2.createTrackbar('T','image',0,255,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

# returns True if a entire x is above a threshold value T
def is_pixel_row_white(x,T):
    for i in x:
        if i<T:
            return False
    return True

# returns True if a entire column x is above a threshold value T   
def is_pixel_column_white(x,T):
    for i in x:
        if i[0]<T:
            return False
    return True

# This is a automatic allign the heights of the alphabets
# For example 'p' is written lower than 'a'
# The alligning is done by padding with white pixels
def alphabet_vertical_allignment():
    
    alpha = storage_dict[0]
    
    #define all the tall, short and average alphabets
    short = ['g','j','p','q','y']
    average = ['a','c','e','i','m','n','o','r','s','u','v','w','x','z']
    tall = ['b','d','f','h','k','l','t']
    
    # find tallest and shortest alphabet for reference
    tallest = -1
    for ch in tall:
        if(alpha[ord(ch)-97].shape[0] > tallest):
            tallest = alpha[ord(ch)-97].shape[0] 
    shortest = -1
    for ch in short:
        if(alpha[ord(ch)-97].shape[0] > shortest):
            shortest = alpha[ord(ch)-97].shape[0]     
    
    # find the avergae height of all the alphabets belonging to list average 
    summ = 0
    for ch in average:
            summ += alpha[ord(ch)-97].shape[0]
    average_height = summ// len(average)

    # find differences between averages and extremes
    diff_t = tallest - average_height
    diff_s = shortest - average_height
    
    
    # for all the alphabets do padding to make height same
    for i in range(26):
        ch = chr(i+97)
        if ch not in tall:
            padd = np.zeros([diff_t,alpha[i].shape[1]],dtype=np.uint8)
            padd.fill(255)
            alpha[i] = cv2.vconcat([padd, alpha[i]])
        
        if ch not in short:
            padd = np.zeros([diff_s,alpha[i].shape[1]],dtype=np.uint8)
            padd.fill(255)
            alpha[i] = cv2.vconcat([alpha[i],padd])
    
    # store the resulting images 
    storage_dict[0] = alpha
    save_obj(storage_dict,"storage_dict")

def punctiation_vertical_allignment():
    
    punct = storage_dict[1]
    
    #define all the tall, short and average alphabets

    average = [3,4,6,7,9,10,11,12,13,14,15]
    
    summ = 0
    for ch in average:
            summ += punct[ch].shape[0]
    average_height = summ// len(average)

    
    # for all the alphabets do padding to make height same
    for i in [1,2,5,8]:
        padd = np.zeros([average_height - punct[i].shape[0] ,punct[i].shape[1]],dtype=np.uint8)
        padd.fill(255)
        punct[i] = cv2.vconcat([padd, punct[i],padd])
    
    for i in [0]:
        padd = np.zeros([(average_height - punct[i].shape[0])//2 ,punct[i].shape[1]],dtype=np.uint8)
        padd.fill(255)
        punct[i] = cv2.vconcat([padd, punct[i], padd])
        
    # store the resulting images 
    storage_dict[1] = punct
    save_obj(storage_dict,"storage_dict")


# This function crops the image of each character by removing extra white 
# pixels on the border

def process_characters(x, i, T, img_crop):
    
    # remove completely white rows from the top
    y_top = 0
    while  y_top<len(img_crop):
        if is_pixel_row_white(img_crop[y_top],T):
            y_top+=1
        else:
            break
            
    # remove completely white rows from the bottom
    y_bottom = len(img_crop)-1
    while y_bottom >0:
        if is_pixel_row_white(img_crop[y_bottom],T):
            y_bottom-=1
        else:
            break  
          
    img_crop = img_crop[y_top:y_bottom, 0:img_crop.shape[1]]

    return img_crop

# This is the main segmentation function, that is the function that is used to 
# classify the characters into alphabets, punctiation and numbers 
# and segment them 
    
def apply_segmentation(img,T, save):
    
    global storage_dict
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
    
    # iterate over all character classes to segment them separately into
    # individual characters
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
            if save :           
                storage_dict[x][i]=  process_characters(x, i , T,img_backup[temp[0][0]:temp[1][0]+1,temp[0][1]:temp[1][1]+1])
            else:
                cv2.rectangle(img, pt1=(temp[0][1],temp[0][0]), pt2=(temp[1][1],temp[1][0]),color=(0,255,255),thickness=1)  
    if save:
        save_obj(storage_dict,"storage_dict")
        return
        
    return img



# The main loop for the opencv intercative window
t = -1
s = -1

while(1):
    t = cv2.getTrackbarPos('T','image')
    s = cv2.getTrackbarPos(switch,'image')
    
    (thresh, img) = cv2.threshold(imgray, t, 255, cv2.THRESH_BINARY)
    
    if(s==1): 
        img1 = apply_segmentation(img.copy(),t, False)
        cv2.imshow('image',img1)
    else:
        cv2.imshow('image',img)
        
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

# If s is 1, it means we have to save the character sample    
if s==1:
    # apply segmentation with save set to True
    apply_segmentation(img,t, True)
    # align the saved character samples
    alphabet_vertical_allignment()
    punctiation_vertical_allignment()
    cv2.destroyAllWindows()
