from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

url = "https://facebook.com/public?query=電子菸&type=pages&init=dir&nomc=0"

r1 = requests.Session()
r = r1.get(url)
#print(r.text)

soup = BeautifulSoup(r.text, "html.parser")
#print(soup)
hidden = soup.find_all(class_="hidden_elem")
#print(hidden)
code = soup.find_all("code", id="u_0_f")
print(code)
