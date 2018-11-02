import os,shutil,requests,re,csv,time
from bs4 import BeautifulSoup as bs
from logger import log
from hyper.contrib import HTTP20Adapter

def get_data(link):
	log.info('Extracting droplist data.')
	#try to get html from the droplist page.
	count = 0
	while count < 5:
		try:
			r = s.get(link,headers=headers)
			soup = bs(r.text,'html.parser')
			break
		except Exception as e:
			log.error(e)
			log.info('Retrying.')
			time.sleep(3)
		count += 1
	#getting neccessary info from the html.
	for items in soup.find_all('div',{'class':'card-2'}):
		try:
			name = items.find('div')['data-itemname']
			img = 'https://supremecommunity.com' + str(items.find('img')['src'])
			usd = '$ ' + items.find('p',{'class':'priceusd'}).text
			gbp = '£ ' + items.find('p',{'class':'pricegbp'}).text

			log.info('\n{}\n{}\n{}\n{}\n'.format(name,img,usd,gbp))
			
			#create a dict with item as key and prices in a list as values
			final.setdefault(name,[]).append(usd)
			final[name].append(gbp)

			#downloading pictures
			log.info('downloading {}.jpg'.format(name))
			current_path = os.getcwd()
			#replacing any characters not allowed in filenames ie: '/','?' etc with 'space'
			filename = re.sub(r"[\\\/\:\*\?\"\<\>\|]+"," ",str(name)+'.jpg')
			image = s.get(img,headers=headers,stream=True)
			path = os.path.join(current_path,"images",filename)
			with open(path,"wb") as out_file:
				shutil.copyfileobj(image.raw, out_file)
				del image

			log.success('Done!')
		except:
			log.error('Error downloading {}! Please retry.'.format(name))
			pass

	with open('items.csv','w+',newline='') as f:
		writer = csv.writer(f)
		writer.writerow(["items","USD","GBP"])
		for name,prices in final.items():
			writer.writerow([name,prices[0],prices[1]])
			
		log.success('All items written into csv!')



#Start of the program
#####################################################
final = {}

log.success('-----------------------------------')
log.success('          sc-retails')
log.success('         Written by @ymmxl')
log.success('-----------------------------------')
log.success('\n')
log.info('Initializing.')

#url = str(input('Welcome! link please.\n'))
s = requests.Session()
s.mount('https://www.supremecommunity.com', HTTP20Adapter())
headers = {
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'upgrade-insecure-requests':'1'
}


log.info('Fetching data.\n')
res = s.get('https://www.supremecommunity.com/season/latest/droplists/',headers=headers)
soup = bs(res.text,'html.parser')
new = soup.find('div',{'id':'box-latest'}).find('a')['href']
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

