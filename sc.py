import os,shutil,requests,re,csv
from bs4 import BeautifulSoup as bs
from logger import log
from hyper.contrib import HTTP20Adapter

final = {}

print('-----------------------------------')
print('          sc-retails')
print('         Written by @ymmxl')
print('-----------------------------------')
print('\n')
log.info('Initializing.')

url = str(input('Welcome! link please.\n'))
s = requests.Session()
s.mount('https://www.supremecommunity.com', HTTP20Adapter())
headers = {
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'upgrade-insecure-requests':'1'
}


#img = 'https://supremecommunity.com/u/season/add/20180925/976a446b862648c1a29bae7fbf255cc2_sqr.jpg'

r = s.get(url,headers=headers)
soup = bs(r.text,'html.parser')

for items in soup.find_all('div',{'class':'card-2'}):
	try:
		name = items.find('div')['data-itemname']
		img = 'https://supremecommunity.com' + str(items.find('img')['src'])
		usd = '$ ' + items.find('p',{'class':'priceusd'}).text
		gbp = '£ ' + items.find('p',{'class':'pricegbp'}).text

		log.info('\n{}\n{}\n{}\n{}\n'.format(name,img,usd,gbp))
		log.info('downloading {}.jpg'.format(name))
		#create a dict with item as key and prices in a list as values
		final.setdefault(name,[]).append(usd)
		final[name].append(gbp)

		#downloading pictures
		current_path = os.getcwd()
		filename = re.sub(r"[\\\/\:\*\?\"\<\>\|]+"," ",str(name)+'.jpg')
		image = s.get(img,headers=headers,stream=True)
		path = os.path.join(current_path,"images",filename)
		with open(path,"wb") as out_file:
			shutil.copyfileobj(image.raw, out_file)
			del image

		log.success('Done!')
	except:
		log.error('Error!')
		pass

with open('items.csv','w+',newline='') as f:
	writer = csv.writer(f)
	writer.writerow(["items","USD","GBP"])
	for name,prices in final.items():
		writer.writerow([name,prices[0],prices[1]])
		
	log.success('All items written into csv!')