import cv2
from PIL import Image,ImageFont,ImageDraw
import numpy as np
import pytesseract
from pdftojpg import pyMuPDF_fitz
import image
import os


userinput_start = "2020年7月24日"
userinput_end = "2020年7月25日"
userinput_price = ""
userinput_country = ""


total = []
allprice = []
date = []

def finaltotalprice (data):
    temp = []
    for x,b in enumerate(data.splitlines()):
        if x!=0:
            b = b.split()
            #print(b)
            if len(b)==12:
                if b[11]=="總" or b[11]=="总":
                    temp.append(b)
                    col = b[7]
                    break
    for x,b in enumerate(data.splitlines()):
        if x!=0:
            b = b.split()
            tmp = int(b[7])
            col = int(col)
            if len(b)==12:
                if tmp in range(col-10,col+10):
                    total.append(b[11])
                #if tmp==col or tmp==col+1 or tmp==col-1:
                    #total.append(b[11])

def takeprice(a,text):
    price = ""
    for i in range(a+1,len(text)):
        temp = text[i]
        if temp=="0" or temp=="1" or temp=="2" or temp=="3" or temp=="4" or temp=="5" or temp=="6" or temp=="7" or temp=="8" or temp=="9":
            price = price + temp
        elif temp==".":
            price = price + text[i:i+3]
            allprice.append(price)
            a = a + 1
            findprice(text,a)
            break

def findprice(text,a):
    for i in range(a,len(text)):
        temp = text[i]
        if i+1 >= len(text):
            break
        if temp == "$":
            takeprice(i,text)
            break 

def finddate(start, end, text):
    if text.find(start)==-1 or text.find(end)==-1:
        return "F"
    else :
        return "T"

def deletesameprice(allprice):
    newallprice=[]
    for i in allprice:
        if not i in newallprice:
            newallprice.append(i)
    allprice.clear()
    for i in newallprice:
        i = float(i)
        allprice.append(i)
    return allprice

def checkprice(allprice,finalprice):
    tmp=0.00
    for i in range(len(allprice)-1):
        tmp=tmp+float(allprice[i])
    a=len(allprice)
    tmp=round(tmp,2)
    if float(tmp)==float(allprice[a-1]) or float(tmp)==finalprice:
        return "T"
    else:
        return "F"



#pdf to jpg 
r = open("./image/count.txt",'r')
count = r.read()
r.close
if __name__ == "__main__":
    pdfPath = './airbnb.pdf'
    imagePath = './image'
    photofilePath = pyMuPDF_fitz(pdfPath, imagePath, count)
print(photofilePath)

#讀取每一張圖片
flag = 0
for lists in os.listdir(photofilePath):
    photo = os.path.join(photofilePath,lists)
    img = cv2.imread(photo)
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #(b,g,r) = cv2.split(img) #彩色equalizehist
    #bH = cv2.equalizeHist(b)
    #gH = cv2.equalizeHist(g)
    #rH = cv2.equalizeHist(r)
    #eqimg = cv2.merge((bH,gH,rH))
    eqimg = cv2.equalizeHist(img_g) #黑白equalizehist
    #cv2.imwrite("./cvphoto.jpg",eqimg)
    temp = pytesseract.image_to_string(eqimg, lang='chi_tra+eng+chi_sim')
    temp = temp.replace(" ","")
    temp = temp.replace("\n"," ")
    temp = temp.replace(" ","")
    tmp = pytesseract.image_to_data(eqimg,lang='chi_tra+eng+chi_sim')
    if flag:
        text += temp
        data += tmp
    else:
        flag = 1
        text = temp
        data = tmp
#print("辨識內容:")
#print(text)
#print(data)
r = open("./tesseract_data.txt",'w',encoding="utf-8") #check data
r.write(data)
r.close

if text.find("Airbnb")!=-1:
    finaltotalprice(data) #找總價錢
    print(total)
    temp=total[len(total)-1] #拿到總價(數字)
    temp=temp[1:]
    i = 0
    for i in range(len(temp)-1): #去逗號
        if temp[i]==",":
            finalprice=temp[:i]+temp[i+1:]
    finalprice=float(finalprice)
    findprice(text,0) #找所有$號後面的價錢
    allprice=deletesameprice(allprice) #刪掉相同的價錢
    allprice=sorted(allprice,reverse=False) #排序
    print(allprice)
    print("price is:"+checkprice(allprice,finalprice))
    date = finddate(userinput_start,userinput_end,text)
    print("date is:"+date)
elif text.find("UberEats")!=-1: #UberEats
    date = []
    finaltotalprice(data)
    decimal = 0.00
    if total[len(total)-1]!='00' and total[len(total)-1].find("$")==-1: #記錄小數點後數字
        decimal = float(total[len(total-1)])
    for i in total: #找到總價錢并轉換為float
        if i.find("$")!=-1:
            temp = i
            tmp = i.find("$")
    finalprice = float(temp[tmp+1:]) + decimal #總價 = finalprice

    for x,b in enumerate(data.splitlines()): #找到日期
        b = b.split()
        if len(b)==12 and b[0]!="level": 
            if b[11]=="Uber":
                col = int(b[7])
    for x,b in enumerate(data.splitlines()):
        b = b.split()
        if len(b)==12 and b[0]!="level":
            if int(b[7]) in range(col-50,col+50):
                date.append(b[11])
    temp = ""
    for i in range(len(date)-1,len(date)-5,-1):
        if i == len(date)-1:
            temp+=date[i]
        else:
            temp = temp+'|'+date[i]
    i = 0
    while 1: #刪掉與日期無關的字元
        if i==len(temp):
            i = 0
            break
        if ord(temp[i])not in range(ord("0"),ord(":")) and temp[i]!="|":
            temp=temp[:i]+temp[i+1:]
        elif temp[i]==",":
            temp=temp[:i]+temp[i+1:]
        else:
            i+=1
    while 1: #判斷是否有兩個"|"連在一起
        if i==len(temp)-2:
            i = 0
            break
        if temp[i]=='|' and ord(temp[i])==ord(temp[i+1]):
            temp = temp[:i+1]+temp[len(temp)-1]+'|'
            break
        else:
            i+=1
    print(temp)
    daterule = ['年','月','日']
    flag = 0
    dateans = ""
    for i in range(len(temp)): #月和日位置交換
        if temp[i]=="|"and flag == 1:
            b = i
            dateans = temp[:a]+temp[b:len(temp)-1]+temp[a:b]+temp[len(temp)-1]
            flag = 0
            break
        elif temp[i]=="|":
            a = i
            flag = 1
    for i in range(len(dateans)): #把分隔符號換做年月日
        if dateans[i]=="|":
            dateans = dateans[:i]+daterule[flag]+dateans[i+1:]
            flag+=1
    print(dateans)
    print(finalprice)
    print(total)
    #findprice(text,0)
    #deletesameprice(allprice)  不確定要不要
    #allprice=sorted(allprice,reverse=False)

    


#imgpath = r"C:\Users\user\Desktop\專題\airbnb.jpg"
#cv2.namedWindow(imgpath, cv.WINDOW_NORMAL)
#cv2.resizeWindow(imgpath, 3300, 2550)
#cv2.imshow(imgpath,fin)
#cv2.waitKey(0)
