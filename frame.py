from __future__ import division
import cv2  
import numpy as np
import sys
import MySQLdb

def limx(x,x0,x1):
    global w
    if x<x0: return 1
    elif x>x1: return w-1
    return x

def limy(y,y0,y1):
    global h
    if y<y0: return 1
    elif y>y1: return h-1
    return y
    
def truncx(x,w):
    if x>w-150: return w-150
    return x
    
def truncy(y):
    if y<20: return 20
    return y

    
# mouse callback function  
def draw(event,x,y,flags,param):  
    global ix,iy,ox,oy,tx,ty,w,h
    global drawing,playing
    global txt, name, font, i  
    global img0, img1
    
    if event == cv2.EVENT_LBUTTONDOWN:  
        drawing = True  
        ix = limx(x,5,w-6)  
        iy = limy(y,5,h-6)  

    elif event == cv2.EVENT_MOUSEMOVE:  
        if drawing == True:  
            img = img0.copy()
            ox = limx(x,5,w-6)  
            oy = limy(y,5,h-6)  
            tx = truncx(ix,w)
            ty = truncy(iy)
            cv2.rectangle(img,(ix,iy),(ox,oy),(0,255,0),1)
            cv2.putText(img, name, (tx,ty), font, 1, (0,0,255),1)
        else:
            img = img1.copy()
            cv2.line(img,(x,0),(x,h),(0,255,0),1)
            cv2.line(img,(0,y),(w,y),(0,255,0),1)
            cv2.putText(img, name, (truncx(x,w),truncy(y)), font, 1, (0,0,255),1)

        # show name
            
        cv2.imshow('image',img)

    elif event == cv2.EVENT_LBUTTONUP:  
        drawing = False  
        img = img0.copy()
        ox = limx(x,5,w-6)  
        oy = limy(y,5,h-6)  
        tx = truncx(ix,w)
        ty = truncy(iy)
        
        cv2.rectangle(img,(ix,iy),(ox,oy),(0,255,0),1)
        cv2.putText(img, name, (tx,ty), font, 1, (0,0,255),1)
        cv2.imshow('image',img)
        img1 = img.copy()
        
        print ix,iy,ox,oy
        if playing == False:
            x = (ix+ox)/w/2
            y = (iy+oy)/h/2
            dx = (ox-ix)/w
            dy = (oy-iy)/h
            txt = sql.format(i,name, x,y, dx,dy)
            


# read imput image
i = int(sys.argv[1])
project = sys.argv[2]
fname = sys.argv[3]

img0 = cv2.imread('{}/{}.jpg'.format(project,fname))
img1 = img0.copy()
#cv2.namedWindow('image',cv2.WINDOW_NORMAL)  
cv2.namedWindow('image',cv2.WINDOW_AUTOSIZE)  
cv2.setMouseCallback('image',draw)
cv2.imshow('image',img0)
h,w = img0.shape[:-1]

font=cv2.FONT_HERSHEY_SIMPLEX

conn = MySQLdb.connect("localhost","root","123","images" )
cursor = conn.cursor()

sql='INSERT INTO t1 VALUES ({},"{}",{},{},{},{});'
txt=''

name = 'press KEY for class'
names = { ord('1'): 'car' }

ks = set(names.keys())
          
# mouse drawback
drawing = False # true if mouse is pressed  
playing = True
ix,iy = 0,0
ox,oy = 0,0
tx,ty = 0,0
while(1):  
    k = cv2.waitKey(1) & 0xFF  
    if k == 27: # press ESC
        break
    elif k==ord('s') and not playing: # press s
        print '!!!', txt
        cursor.execute(txt)
        print name,'data written.'
        break  
    elif k in ks:
        if playing:
            print 'header written.'
            playing = False
        else:
            cv2.rectangle(img0,(ix,iy),(ox,oy),(0,0,255),1)
            cv2.putText(img0, name, (tx,ty), font, 1, (0,0,255),1)
            print '!!!', txt
            cursor.execute(txt)
            print name,'data written.'

        name = names[k]
        

cursor.close()
conn.commit()
conn.close()
print 'file saved'
        

cv2.destroyAllWindows()

