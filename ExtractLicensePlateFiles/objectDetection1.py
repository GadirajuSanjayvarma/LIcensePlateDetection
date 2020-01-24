from importModules1 import *
from helperFunctions1 import *
import pytesseract as tess
import numpy as np 
import os
tess.pytesseract.tesseract_cmd=r'C:\MachineLearning\Tesseract\tesseract.exe'
cap = cv2.VideoCapture("ourexample.mp4")
path='C:\MachineLearning\ExtractedLicense'
count=0
list1=[]
while(cap.isOpened()):
    fps = (int)(cap.get(cv2.CAP_PROP_FPS))
    #print(fps)
    ret, frame = cap.read()
    for i in range(0,fps):
        ret, frame = cap.read()
    if(ret == True):
        ret, frame1 = cap.read()
        #err = np.sum((frame.astype("float") - frame1.astype("float")) ** 2)
	    #err =err/float(frame.shape[0] * frame.shape[1])
        #print(err)
        image,ymin,xmin,ymax,xmax=run_detector(detector,frame)
        w,h,c=image.shape
        cv2.imshow('image',image)
        cv2.waitKey(fps)
        '''k=cv2.waitKey()
        if(k==48):
            break'''
        if(ymin!=1 or xmin!=1 or ymax!=1 or xmax!=1):
            lim_ymin=int(round(w*ymin,0))
            lim_xmin=int(round(h*xmin,0))
            lim_ymax=int(round(w*ymax,0))
            lim_xmax=int(round(h*xmax,0))
        #print("sizes:")
        #823 556 883 622
            #print(lim_ymin,lim_xmin,lim_ymax,lim_xmax)
            crop = image[lim_ymin:lim_ymax+2,lim_xmin:lim_xmax+4]
            #cv2.imwrite(os.path.join(path , "frame%d.jpg" % count),crop)  
            #gray = cv2.cvtColr(crop, cv2.COLOR_BGR2GRAY)
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        #print(lim_ymin,lim_ymin+lim_ymax,lim_xmin,lim_xmin+lim_xmax)
            #print("printing license part of image")
            mask = np.zeros((3, 3), np.uint8)
            opening = cv2.morphologyEx(gray, cv2.MORPH_CLOSE,mask,iterations=1)
            #opening=cv2.Canny(crop,100,200)
            text=tess.image_to_string(opening, lang='eng',config='--psm 7')
            #print(len(text))
            if(text):
                s=''
                #print("License plate is:")
                #cv2.imshow('window',opening)
                for i in text:
                    if((ord(i)>=48 and ord(i)<=57) or (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90)):
                        s+=i
                #print(s)
                if(s not in list1 and len(s)==10):
                    cv2.imshow('window',opening)
                    print("License plate is:")
                    #print(len(s))
                    count+=1
                    cv2.imwrite(os.path.join(path , "frame%d.jpg" % count),crop)
                    print(s)
                    list1.append(s)                    
                
    else:
        break

                        


    #else:
        #cv2.imshow('image',image)
        '''if cv2.waitKey(0):
            break'''

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()










