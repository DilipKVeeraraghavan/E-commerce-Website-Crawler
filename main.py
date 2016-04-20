import requests
from bs4 import BeautifulSoup
import urllib2

fw=open('example.txt','w')

def ebay_categories(max_pages):
    page=1
    while page < max_pages:
        url = 'http://www.ebay.in/'
        source_code = requests.get(url)
        plain_text = source_code.text
        obj = BeautifulSoup(plain_text,'html.parser')
        for link in obj.findAll('a',{'class':'rt'}):
            title = link.string
            href = link.get('href')
            print(href)
            print(title)
            fw.write("\nCategory : "+title+"\n")
            fw.write(href+"\n\nSub Categories :\n")
            for sublink in obj.findAll('a'):
                if(sublink.get('title')!= None):
                    if(title in sublink.get('title')):
                        subtitle = sublink.get('title')
                        subhref = sublink.get('href')
                        fw.write(subtitle.encode('ascii','ignore')+"\n")
                        print(subtitle)
                        fw.write(subhref+"\n\n")
                        print(subhref+"\n")
            print("------------------------------------------\n")
            fw.write("------------------------------------------\n")

        page +=1

def ebay_items(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    obj = BeautifulSoup(plain_text,'html.parser')
    for link in obj.findAll('a',{'itemprop':'name'}):
        href = "https://www.ebay.in"+link.get('href')
        ebay_enterItemPage(href)


def flipkart_items(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    obj = BeautifulSoup(plain_text,'html.parser')
    for link in obj.findAll('a',{'class':'fk-display-block'},{'data-tracking-id':'prd_title'}):
        newhref = link.get('href')
        if('/' in newhref):
            href = 'https://www.flipkart.com'+newhref
            print(link.get('title'))
            flipkart_enterItemPage(href)


def amazon_items(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    obj = BeautifulSoup(plain_text,'html.parser')
    for link in obj.findAll('a',{'class':'a-link-normal s-access-detail-page  a-text-normal'}):
        newhref = link.get('href')
        amazon_enterItemPage(newhref)



def amazon_enterItemPage(url):
    try:
        urllib2.urlopen(url)
        source_code = requests.get(url)
        plain_text = source_code.text

        obj = BeautifulSoup(plain_text,'html.parser')
        for link in obj.findAll('span',{'id':'productTitle'}):
            title = link.string
            print(title)
            fw.write("Title : "+title +'\n')
            for sublink in obj.findAll('img',{'id':'landingImage'}):
                img = sublink.get('src')
                print("Image URL : " +img+'\n')
                fw.write("Image URL : " +img+'\n')
            for newsublink in obj.findAll('div',{'id':'avgRating'}):
                stars = newsublink.string
                if(stars != None):
                    print("Rating : " +stars+'\n')
                    fw.write("Rating : " +stars+'\n')
        for link in obj.findAll('span',{'id':'priceblock_saleprice'}):
            price = link.string
            if(price != None):
                print("Price :"+price+'\n\n')
                fw.write("Price :"+price+'\n\n')
        fw.write(' - - - - - - - - - - - - - - - - - - - ')
    except urllib2.HTTPError, e:
        print("Error in connection !")
    except urllib2.URLError, e:
        print("Junk URl neglected !")


def flipkart_enterItemPage(url):
    try:
        urllib2.urlopen(url)
        source_code = requests.get(url)
        plain_text = source_code.text

        obj = BeautifulSoup(plain_text,'html.parser')
        for link in obj.findAll('span',{'class':'title'},{'itemprop','name'}):
            title = link.string
            print(title)
            fw.write("Title : "+title +'\n')
            for sublink in obj.findAll('img',{'class':'productImage  current'}):
                img = sublink.get('src')
                print("Image URL : " +img+'\n')
                fw.write("Image URL : " +img+'\n')
            for newsublink in obj.findAll('div',{'class':'bigStar'}):
                stars = newsublink.string
                print("Rating : " +stars+'\n')
                fw.write("Rating : " +stars+'\n')
        for link in obj.findAll('div',{'class':'selling-price omniture-field'}):
            price = link.string
            print("Price :"+price+'\n\n')
            fw.write("Price :"+price+'\n\n')
        fw.write(' - - - - - - - - - - - - - - - - - - - ')
    except urllib2.HTTPError, e:
        print("Error in connection !")
    except urllib2.URLError, e:
        print("Junk URl neglected !")


def ebay_enterItemPage(url):
    try:
        urllib2.urlopen(url)
        source_code = requests.get(url)
        plain_text = source_code.text
        obj = BeautifulSoup(plain_text,'html.parser')
        for link in obj.findAll('span',{'class':'title'},{'itemprop','name'}):
            title = link.string
            print(title)
            fw.write("Title : "+title +'\n')
            for sublink in obj.findAll('img',{'itemprop':'image'}):
                if(title in sublink.get('title')):
                    img = sublink.get('src')
                    print("Image URL : " +img+'\n')
                    fw.write("Image URL : " +img+'\n')
        for link in obj.findAll('div',{'class':'topPriceRange'},{'itemprop':'price'}):
            price = link.string
            print("Price :"+price+'\n\n')
            fw.write("Price :"+price+'\n\n')
        fw.write(' - - - - - - - - - - - - - - - - - - - ')

    except urllib2.HTTPError, e:
        print("Error in connection !")
    except urllib2.URLError, e:
        print("Junk URl neglected !")




fw=open('example.txt','w')
url = raw_input("Enter the url :")
fw.write('CATEGORIES : \n ----------------------------------------')
ebay_categories(2)
fw.write('\n\nPRODUCTS : \n ----------------------------------------\n\n')
if("ebay" in url):
    ebay_items(url)
elif("amazon" in url):
    amazon_items(url)
elif("flipkart" in url):
    flipkart_items(url)
else:
    print("Invalid input !")