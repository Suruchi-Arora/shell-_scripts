from cmath import nan
from itertools import count
from types import NoneType
from unittest import TestCase
import cv2
from PIL import Image
from pytesseract import pytesseract
from datetime import datetime
import time
import pandas as file
import os
import re

df=file.DataFrame()
filename='Teachersdata.csv'
if os.path.exists(filename):
    pass 
else:
    data=[{
        'Teacher ID':'',
        'Entry Time':'',
        'Entry Date':''
    }]
    d=file.DataFrame(data)
    d.to_csv(filename,index=False)
used_codes=[]
entries_list=[]
entry_time=[]
exit_time=[]
date=[]
exitDate=[]
cap = cv2.VideoCapture(1)

def tesseract():
    image_path='test1.jpg'
    pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text=pytesseract.image_to_string(Image.open(image_path))

    print(text)

    print("Extracting numbers......")
    numbers = re.findall('[0-9]+', text)
    print(numbers)
    if len(numbers)==0:
        camera()
    for i in numbers:
        if len(i)==5:
            print(i)
            global teacherId
            teacherId=i
            break
        else:
            camera()
    if teacherId not in used_codes:
        
        # display on the screen
        print('Approved. you can enter!')

        #printing code on the screen
        
        used_codes.append(teacherId)
        #printing date and time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        entry_time.append(current_time)
        current_date=now.strftime("%B %d, %Y")
        date.append(current_date)

        entries_list.append(teacherId)

        #storing code in excel
        df['Teacher ID'] = entries_list[0::100]
        df['Entry Time']= entry_time[0::100]
        df['Entry Date']=date[0::100]

        save_file=file.read_csv(filename)
        total=len(save_file.index)
        save_file.loc[total,'Teacher ID']=teacherId
        save_file.loc[total,'Entry Time']=current_time
        save_file.loc[total,'Entry Date']=current_date
        save_file.to_csv(filename,index=False)


        if teacherId not in entries_list:
            entries_list.append(teacherId)
        print(save_file.loc[total])
        print(teacherId)
        time.sleep(3)

    elif teacherId in used_codes:
        print('Approved. you can leave!')
        print(teacherId)
        used_codes.remove(teacherId)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        exit_time.append(current_time)
        current_date=now.strftime("%B %d, %Y")
        exitDate.append(current_date)
    
        #storing code in excel
        df['Teacher ID'] =entries_list[0::100]
        df['Exit Time']=exit_time[0::100]            
        df['Exit Date']=exitDate[0::100]
        print("exit time: ",current_time, " Exit date: ",current_date)

        save_file=file.read_csv(filename)
        ExitColumnData=save_file['Exit Time']
        pointer=save_file.loc[save_file['Teacher ID'] == float(teacherId)].index
        pointer=pointer[-1]
        save_file.loc[pointer,'Teacher ID']=teacherId
        save_file.loc[pointer,'Exit Time']=current_time
        save_file.loc[pointer,'Exit Date']=current_date
        save_file.to_csv(filename,index=False)

        time.sleep(3)
    else:
        pass

def camera():
    while(True):
        _, image = cap.read()
        cv2.imshow('image', image)
        if cv2.waitKey(1) & 0xff==ord('s'):
            cv2.imwrite('test1.jpg',image)
            tesseract()
camera()
cap.release()
cv2.destroyAllWindows()           
cv2.waitKey()
# tesseract()




