import pandas as pd
import requests
from bs4 import BeautifulSoup

companies=[]
street_addresses=[]
cities=[]
states=[]
pincodes=[]
contact_persons=[]
phones=[]

url='http://www.indiabusinesstoday.in/category/plant-and-machinery-1-834/'

page=range(10,501,10)
urllist=[url]
for item in page:
    urllist.append(url+str(item))

for url in urllist:

    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    table = soup.find_all('div', {'class':'col-sm-12'})
    phone=soup.find_all('strong')
    for phone in phone:
        if phone.text=='Phone No: ':
            phone=phone.next_sibling
            phones.append(phone)
            
    for i in range(7,len(table)):

        if table[i].find('div',{'class':'row col-sm-12'}):

            print table[i].find('a').text
            companies.append(table[i].find('a').text)
            
            sub_url=table[i].find('a')['href']
            sub_response = requests.get(sub_url)
            sub_html=sub_response.content
            sub_soup=BeautifulSoup(sub_html)
            street_address=sub_soup.find('span',{'itemprop':'streetAddress'})
            street_addresses.append(street_address.text)
            
            city=sub_soup.find('span',{'itemprop':'addressLocality'})
            cities.append(city.text)
            
            pincode=city.next_sibling
            pincodes.append(pincode)
            
            state=sub_soup.find('span',{'itemprop':'addressRegion'})
            states.append(state.text)
            
            person=sub_soup.find('span',{'class':'glyphicon-user'})
            person=person.find_next('span')
            contact_persons.append(person.text.strip())


companies_df=pd.DataFrame({'Company':companies,'Contact Name':contact_persons,
                            'Street Address':street_addresses,'City':cities,
                            'State':states,'Pincode':pincodes,'Contact No.':phones})

companies_df.to_csv('scraped_data.csv')