from bs4 import BeautifulSoup
import requests
import urllib.parse
query = input("enter your query: ")

url = "https://www.quora.com/search?q="+urllib.parse.quote(query)
r= requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
fact=soup.find(class_="kno-rdesc")
print(fact.text)
#print(soup.prettify())
#for item in div_bs4 in range(0,1):
#    print(item.getText())
#print("------------------")
#print(soup.prettify)


