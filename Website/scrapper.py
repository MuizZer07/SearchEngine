from lxml import html  
import csv,os,json
import requests
import re
import pandas
import fire

#from exceptions import ValueError
from time import sleep

def AmzonParser(url, inn):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)
    while True:
        sleep(5)
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
            XPATH_IMAGE = '//img[@id="landingImage"]/@data-a-dynamic-image'
            XPATH_BRAND = '//*[@id="bylineInfo"]//text()'
            XPATH_feature = '//*[@id="feature-bullets"]//text()'
            XPATH_SIM = '//div[@id="sp_detail"]/@data-a-carousel-options'
            XPATH_RAT='//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()'
            
            

 
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            RAW_IMAGE = doc.xpath(XPATH_IMAGE)
            RAW_BRAND = doc.xpath(XPATH_BRAND)
            RAW_feature = doc.xpath(XPATH_feature)
            RAW_SIM=doc.xpath(XPATH_SIM)
            RAW_RAT=doc.xpath(XPATH_RAT)

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
            IMAGE = ''.join(RAW_IMAGE) if RAW_IMAGE else None
            BRAND = ''.join(RAW_BRAND) if RAW_BRAND else None
            str1 = ''.join(RAW_feature) if RAW_feature else None
            sim = ''.join(RAW_SIM) if RAW_SIM else None
            RAT = ''.join(RAW_RAT) if RAW_RAT else None



            nImage=""
            nImage1=""
            newimg=""
            listnew=[]
            if(sim):
                newimg=sim.split("[")
                sim=newimg[1]
                newimg=sim.split("]")
                sim=newimg[0]
                newimg = sim.split('\"')
                for i in range(len(newimg)):
                    if(i%2==1):
                        listnew.append(newimg[i])

            
            #newimg1 = newimg[1]
            listImage=[]
            if(IMAGE):
                nImage=IMAGE.split("_")
                for i in range(len(nImage)):
                    if(i%2==1):
                        nImage1="https://images-na.ssl-images-amazon.com/images/I/618OXolXPjL._"+nImage[i]+"_.jpg"
                        listImage.append(nImage1) 
            lst=[] 
            if(str1):
                len1 = len(str1)-1
                s = str1[318:len1]
                s = s.replace("\t", '')
                s=s.split("\n")
                s = list(filter(None,s))
                for srg in s:
                    if(srg[0]!=' '):
                        lst.append(srg)        
 
            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE
 
            if page.status_code!=200:
                raise ValueError('captha')
            data = {
                    'asin':inn,
                    'title':NAME,
                    'brand':BRAND,
                    'feature':lst,
                    'price':SALE_PRICE,
                    'original_price':ORIGINAL_PRICE,
                    'availability':AVAILABILITY,
                    'url':url,
                    'Image':listImage,
                    'catagories':CATEGORY,
                    'similar':listnew,
                    'rating':RAT
                    }
 
            return data
        except Exception as e:
            print(e)
 
def ReadAsin():
    AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"out.csv")))
    #df = pandas.read_csv('product.csv')
    #lst=df['similar']
    #print(lst)
    extracted_data = []
    #print(df)
    f=open('data.json','w')
    k=0
    for i in AsinList:
        k+=1
        url = "http://www.amazon.com/dp/"+str(i['B00119TXES'])
        print("Processing: "+url)
        temp = AmzonParser(url, str(i['B00119TXES']))
        extracted_data.append(temp)
        json.dump(extracted_data,f,indent=4)
        fire.firework(temp)
        if(k%20==0):
            print("New 20 value added k=", k)
            sleep(30)