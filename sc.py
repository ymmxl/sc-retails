import os,shutil,requests,re,csv,time,sys
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from logger import log
from requests.packages import urllib3
import gsheets as gsheets
urllib3.disable_warnings()
#from hyper.contrib import HTTP20Adapter

def get_data(link):
	log.info('Extracting droplist data.')
	#try to get html from the droplist page.
	count = 0
	while count < 5:
		try:
			r = s.get(link,verify=False)
			soup = bs(r.text,'html.parser')
			break
		except Exception as e:
			log.error(e)
			log.info('Retrying.')
			time.sleep(3)
		count += 1
	#getting neccessary info from the html.
	c=0
	#getting more-infos section on sc
	try:
		bar = soup.find('div',{'id':'catalog-inner'}).findChild().text
		if bar:
			log.success("This week's Extra Info by SC:")
			log.success(bar)
	except Exception as e:
		log.info("failed getting more-info")
		log.info(e)
		pass
	for items in soup.find('div',{'class':'catalog-list'}).findChildren(recursive=False):
		try:
			name = items.attrs["data-name"]
			img = 'https://supremecommunity.com' + str(items.find("div",{"class":"catalog-item__thumb"}).find('img')['data-src'])
			usd = "o"
			gbp = "0"
			try:
				usd = items.attrs["data-usdprice"]
				gbp = items.attrs["data-gbpprice"]
			except KeyError:
				pass
			c+=1
			log.info("\n{}\n{}\n$ {}\n£ {}".format(name,img,usd,gbp))
			
			#create a dict with item as key and prices in a list as values
			final.setdefault(name,[]).append(usd)
			final[name].append(gbp)

			#downloading pictures
			log.info('downloading {}.jpg'.format(name))
			current_path = os.getcwd()
			#replacing any characters not allowed in filenames ie: '/','?' etc with 'space'
			filename = re.sub(r"[\\\/\:\*\?\"\<\>\|]+"," ",str(name)+'.jpg')
			image = s.get(img,verify=False,stream=True)
			path = os.path.join(current_path,"{} Images".format(today),filename)
			with open(path,"wb") as out_file:
				shutil.copyfileobj(image.raw, out_file)
				del image

			log.success('Done!\n')
		except Exception as e:
			log.warning(e)
			log.error('Error downloading {}! Retrying.'.format(name))
			try:
				#downloading pictures
				log.info('downloading {}.jpg'.format(name))
				current_path = os.getcwd()
				#replacing any characters not allowed in filenames ie: '/','?' etc with 'space'
				filename = re.sub(r"[\\\/\:\*\?\"\<\>\|]+"," ",str(name)+'.jpg')
				image = s.get(img,verify=False,stream=True)
				path = os.path.join(current_path,"images",filename)
				with open(path,"wb") as out_file:
					shutil.copyfileobj(image.raw, out_file)
					del image
				pass
			except:
				log.error('Error downloading {}!'.format(name))
			pass
	log.info("{} items found.".format(c))
	with open('items.csv','w+',newline='') as f:
		writer = csv.writer(f)
		writer.writerow(["items","USD","GBP"])
		for name,prices in final.items():
			writer.writerow([name,prices[0],prices[1]]) #strip the signs
			
	log.success('All items written into csv!')

	f = True
	while f:
		log.info("Upload to Sheets? (y/n)")
		upload = str(input())
		if upload == "y":
			f = False
			log.info("Starting upload module.")
			key = gsheets.get_spreadsheet_id()
			done = gsheets.upload()
		elif upload == "n":
			f = False
			done = "exit"
		else:
			log.info("y/n only")
	if done == "DONE":
		log.success("Successfully updated google sheets.")
		log.info("https://docs.google.com/spreadsheets/d/{}".format(key))
	elif done == "exit":
		log.info("Thanks.")
	else:
		log.error("Error updating google sheets.")
		log.warning(done)





#Start of the program
#####################################################
final = {}

log.success('-----------------------------------')
log.success('          sc-retails')
log.success('       Written by @ymmxl')
log.success('-----------------------------------')
log.success('\n')
log.info('Initializing.')
today = dt.now().strftime("%y%m%d")
if not os.path.exists("./{} Images".format(today)):
	log.info("Creating Image directory.")
	os.mkdir("./{} Images".format(today))

#url = str(input('Welcome! link please.\n'))
s = requests.Session()
#s.mount('https://www.supremecommunity.com', HTTP20Adapter())
s.headers.update({
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'upgrade-insecure-requests':'1'
})


log.info('Fetching data.\n')
res = s.get('https://www.supremecommunity.com/season/latest/droplists/',allow_redirects=True,verify=False)

soup = bs(res.text,'html.parser')
new = soup.find('div',{'class':'week-list'}).find('a')['href']
link = 'http://www.supremecommunity.com'+ str(new)
date = new.split('droplist/')[1].replace('/','')

flag = True
while flag:
	log.success('Latest release is {}.'.format(date))
	log.info('Do you want to proceed? (y/n)')
	permission = str(input())
	if permission == 'y':
		flag= False
		get_data(link)
	elif permission == 'n':
		log.info('Thanks.')
		flag = False
	else:
		log.error('Error!')
		log.info("Please input only 'y' or 'n'.")

