import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import pickle

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
        
s_dict  =  load_obj("storage_dict")       
hw_dict= s_dict[0]
pc_dict= s_dict[1]
pc = {"-":0,".":1,",":2,"/":3,"\\":4,":":5,"&":6,"%":7,"^":8,"(":9,")":10,"[":11,"]":12,"@":13,"#":14,"!":15}
nm_dict = s_dict[2]
#nm = {"1":1}
f = open("input.txt", "r")
print(len(hw_dict))
ans = []
max_len = -1
'''
paragh = []
count = 0
for line in f:
    temp_ans = []
    for x in line:
        count+=1
        temp_ans.append(x)
        if(count%80==0):
            paragh.append("".join(temp_ans.copy()))
            temp_ans = []
    paragh.append("".join(temp_ans.copy()))
      
for i in paragh:
    print(i)
f = paragh

'''
for line in f:
    print(line)
    line = line.rstrip().lower()
    
    start = 0
    while(line[start]==" "):
        start+=1
    
    if ord(line[start])-97 in hw_dict:
        im_v = hw_dict[ord(line[start])-97].copy()
    elif line[start] in pc:
        im_v = pc_dict[pc[line[start]]].copy()
    
    
    for x in line[start+1::]:
        if(ord(x)==32):
            prev =   im_v.shape[1]
            space = np.zeros([im_v.shape[0],hw_dict[0].shape[1]],dtype=np.uint8)
            space.fill(255)
            im_v = cv2.hconcat([im_v,space])
            #for j in range(im_v.shape[0]):
            #    im_v[j,prev-1] = 255
        elif(ord(x)>=97 and ord(x)<=122):  
            prev =   im_v.shape[1]
            im_v = cv2.hconcat([im_v,    cv2.resize(hw_dict[ord(x)-97], (hw_dict[ord(x)-97].shape[1], im_v.shape[0]))  ])
            
            #for j in range(im_v.shape[0]):
            #    im_v[j,prev-1] = 255
        elif( x in pc):
            prev =   im_v.shape[1]
            im_v = cv2.hconcat([im_v,    cv2.resize(pc_dict[pc[x]], (pc_dict[pc[x]].shape[1], im_v.shape[0]))  ])           
            #for j in range(im_v.shape[0]):
            #    im_v[j,prev-1] = 255           
    ans.append(im_v)
    if(im_v.shape[1]>max_len):
        max_len = im_v.shape[1]
        
deficit_length = [max_len-x.shape[1] for x in ans]


im_v = ans[0]
space = np.zeros([im_v.shape[0],deficit_length[0]],dtype=np.uint8)
space.fill(255)
im_v = cv2.hconcat([im_v,space])
final = im_v
for i in range(1,len(ans)):
    im_v = ans[i]
    space = np.zeros([im_v.shape[0],deficit_length[i]],dtype=np.uint8)
    space.fill(255)
    im_v = cv2.hconcat([im_v,space])    
    print(final.shape,im_v.shape)
    final = cv2.vconcat([final,im_v])  
      
    


    
while True:
    cv2.imshow('x', final)
    if cv2.waitKey(100) == 27:
        break
cv2.destroyAllWindows()
