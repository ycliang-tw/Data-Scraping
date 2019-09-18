from bs4 import BeautifulSoup
from bs4 import Comment
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import time
import csv

def writecsv(keyword, list_of_dictionaries):
	with open("fb_vape.csv", "a", newline='') as csvfile:
		write = csv.writer(csvfile, delimiter=',')
		write.writerow(['關鍵字', '頁面名稱', '連結網址'])
		for entry in list_of_dictionaries:
			write.writerow([keyword, entry['title'], entry['link']])
		

def scrape_fb_fanpage(keyword):
	url = "https://facebook.com/public?query=" + keyword + "&type=pages&init=dir&nomc=0"
	# use selenium to simulate user behavior
	# open firefox with no display mode (or else will produce error in my current evironment)
	# reference: https://stackoverflow.com/questions/52534658/webdriverexception-message-invalid-argument-cant-kill-an-exited-process-with (2nd answer)
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options=options)	# open firefox
	driver.get(url)
	last_height = driver.execute_script("return document.body.scrollHeight")	# get current window height
	# scroll till the bottom has been reached
	
	pause_time = 3
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(pause_time)
		new_height = driver.execute_script("return document.body.scrollHeight")
		print(new_height)
		if new_height == last_height:
			break
		last_height = new_height
	
	data = driver.page_source
	# parse source html
	soup = BeautifulSoup(data, "html.parser")
	fanpages = soup.find_all(class_="_32mo")
	content = []
	for entry in fanpages:
		info = {
			'link' : entry['href'],
			'title': entry.text
		}
		print(info)
		content.append(info)
	return content



def main():
	search_list = {	
		"電子菸",
		"電子煙",
		"vape"
	}
	data = {}
	for key_word in search_list:
		data = scrape_fb_fanpage(key_word)
		writecsv(key_word, data)
	

if __name__ == '__main__':
	main()
