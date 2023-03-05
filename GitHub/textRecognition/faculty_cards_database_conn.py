import cv2
from PIL import Image
from pytesseract import pytesseract
from datetime import datetime
import time
import re
import mysql.connector

from win32com.client import Dispatch        # for audio
audio = Dispatch("sapi.SpVoice")


mydb=mysql.connector.connect(host="localhost",user="root",database='fac_sams')


mycursor=mydb.cursor()
mycursor.execute("create table if not exists fac_table(Roll_Number varchar(255),Entry_Time time,Entry_Date date,Exit_Time time,Exit_Date date)")

used_codes=[]
entries_list=[]
entry_time=[]
exit_time=[]
date=[]
exitDate=[]
cap = cv2.VideoCapture(0)

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

        audio.Speak("Approved, you can enter!")
        
        used_codes.append(teacherId)
        #printing date and time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        entry_time.append(current_time)
        current_date=now.strftime("%Y-%m-%d")

        sqlform=("insert into fac_table(Roll_Number,Entry_Time,Entry_Date) values (%s,%s,%s)")    
        students=[(teacherId,current_time,current_date)]
        mycursor.executemany(sqlform,students)
        mydb.commit()


    elif teacherId in used_codes:
        print('Approved. you can leave!')
        audio.Speak("Approved, you can leave")

        print(teacherId)
        b=teacherId
        used_codes.remove(teacherId)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date=now.strftime("%Y-%m-%d")
    
        #storing in database --------- 
        sqlform=(f"update fac_table set Exit_Time=%s, Exit_Date=%s where Roll_Number='{b}' and Exit_Time is NULL and Entry_Date=%s")
        students=[(current_time,current_date,current_date)]
        mycursor.executemany(sqlform,students)
        
        mydb.commit()
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




