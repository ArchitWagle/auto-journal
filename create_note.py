import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import pickle

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
        
        
hw_dict= load_obj("storage_dict")[0]

f = open("input.txt", "r")
#print(hw_dict)
ans = []
max_len = -1
for line in f:
    print(line)
    line = line.rstrip().lower()
    im_v = hw_dict[ord(line[0])-97].copy()
    for x in line[1::]:
        if(ord(x)==32):
            space = np.zeros([im_v.shape[0],hw_dict[0].shape[1]],dtype=np.uint8)
            space.fill(255)
            im_v = cv2.hconcat([im_v,space])
        elif(ord(x)>=97 and ord(x)<=122):    
            im_v = cv2.hconcat([im_v, cv2.resize(hw_dict[ord(x)-97], (hw_dict[ord(x)-97].shape[1], im_v.shape[0]))  ])
    ans.append(im_v)
    if(im_v.shape[1]>max_len):
        max_len = im_v.shape[1]
        


      
    


    
while True:
    cv2.imshow('x', im_v)
    if cv2.waitKey(100) == 27:
        break
cv2.destroyAllWindows()
