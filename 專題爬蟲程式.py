#!/usr/bin/env python
# coding: utf-8

# In[6]:


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

input_day = input('請輸入航班日期：')
input_time = input('請輸入航班時間：')
input_num = input('請輸入航班編號：')


Options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webdriver_path = 'C:\\chromedriver.exe'
options = Options()
driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
driver.get("https://zh-tw.flightaware.com/live/fleet/TWB/cancelled") #前往這個網址

time.sleep(2)

search_input = driver.find_element_by_id("s2id_autogen1").send_keys(input_num) #輸入航班號碼

time.sleep(2)

start_search_btn = driver.find_element_by_class_name("orange_button") #按下搜尋
start_search_btn.click()

time.sleep(2)

soup = BeautifulSoup(driver.page_source,"html.parser") 

cancell_char_str='取消'
cancell_flag=0
wrong=0
delay_flag=0
delaytime='此航班無延誤'

try: #爬有後續航班的
    for i in range(2,14):
        day = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div[2]/div[%d]/div[1]/span" %(i)).text #爬日期
        day=day[4:] #修正字串
        print(day)
        if(input_day==day): #輸入日期=需要的日期
            cancell_flag=cancell_flag+1
            delay = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div[2]/div[%d]/div[1]/span" %(i)) #找到指定的航班
            delay.click() #進入該航班資訊
            time.sleep(2)
            try:
                delaytime=driver.find_element_by_xpath("//*[@id='flightPageTourStep1']/div[3]/div[1]/span[3]/div/span").text #爬延遲時間
            except:
                aaa=driver.find_element_by_xpath("//*[@id='slideOutPanel']/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]").text
                delay_flag=1 #沒有延遲時間可以爬 可能取消或輸入錯誤
                
        start = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div[2]/div[%d]/div[2]/div/div/span[2]" %(i)).text #爬出發地點
        print(start)
        
        
        try:
            starttime = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div[2]/div[%d]/div[2]/div/div/span[1]/em/span" %(i)).text #爬出發時間(格式是取消)
        except:
            starttime = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div[2]/div[%d]/div[2]/div/div/span[1]/span" %(i)).text #爬出發時間(格式是未取消)
        
        starttime=starttime[0:5] #修正字串
        
        print(starttime)
        
        end = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div[2]/div[%d]/div[3]/div/div/span[2]" %(i)).text #爬抵達地點
        print(end)
        try:
            endtime = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div[2]/div[%d]/div[3]/div/div/span[1]/em/span" %(i)).text #爬抵達時間
        except:
            endtime = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div[2]/div[%d]/div[3]/div/div/span[1]/span" %(i)).text #爬抵達時間
        
        endtime=endtime[0:5] #修正字串
        
        print(endtime)
        num = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div[2]/div[%d]/div[4]/span" %(i)).text #爬航班編號
        print(num)
        duration = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div[2]/div[%d]/div[5]" %(i)).text #爬航行時間或取消
        print(duration)
        print('\n')
        if((cancell_flag==1)&(duration==cancell_char_str)): #輸入日期的航班取消
            print('此航班已取消')
            break;
        cancell_flag=0
except:
        try: #爬無後續航班的
            for i in range(2,14):
                day = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div/div[%d]/div[1]/span" %(i)).text
                day=day[4:]
                print(day)
                if(input_day==day):
                    cancell_flag=cancell_flag+1
                    delay = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div/div[%d]/div[1]/span" %(i))
                    delay.click()
                    time.sleep(2)
                    try:
                        delaytime=driver.find_element_by_xpath("//*[@id='flightPageTourStep1']/div[3]/div[1]/span[3]/div/span").text
                    except:
                        aaa=driver.find_element_by_xpath("//*[@id='slideOutPanel']/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]").text
                        delay_flag=1 #沒有延遲時間可以爬 可能取消或輸入錯誤
                    
                start = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div/div[%d]/div[2]/div/div/span[2]" %(i)).text
                print(start)
                try:
                    starttime = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div/div[%d]/div[2]/div/div/span[1]/em/span" %(i)).text
                except:
                    starttime = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div/div[%d]/div[2]/div/div/span[1]/span" %(i)).text
                
                starttime=starttime[0:5]
                print(starttime)
                
                end = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div/div[%d]/div[3]/div/div/span[2]" %(i)).text
                print(end)
                try:
                    endtime = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div/div[%d]/div[3]/div/div/span[1]/em/span" %(i)).text
                except:
                    endtime = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div/div[%d]/div[3]/div/div/span[1]/span" %(i)).text
                
                endtime=endtime[0:5]
                
                print(endtime)
                num = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div/div[%d]/div[4]/span" %(i)).text
                print(num)
                duration = driver.find_element_by_xpath("//*[@id='flightPageActivityLog']/div[1]/div/div[%d]/div[5]" %(i)).text
                print(duration)
                print('\n')
                if((cancell_flag==1)&(duration==cancell_char_str)):
                    print('此航班已取消')
                    break;
                cancell_flag=0
        
        except:
            driver.back() #上一頁
            if(i==2):
                print("wrong data")
                wrong=wrong+1 #資料輸入錯誤
            

driver.close()
if((cancell_flag==0) & (wrong!=1)):
    print("此航班在該時段正常飛行") #沒有取消也沒有輸入錯誤
    print(delaytime)


# In[ ]:




