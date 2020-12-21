import requests
import json
def check_stock():

	sku = ['21861756'] #Sku you want to monitor
	#Link for website to checkout 
	link = 'https://www.dickssportinggoods.com/p/breakingt-mens-mookie-of-the-year-grey-t-shirt-20wqtmmlbddgrsgrylada/20wqtmmlbddgrsgrylada'

	headers = {
    	'authority': 'availability.dickssportinggoods.com',
    	'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
   	 'accept': 'application/json',
    	'sec-ch-ua-mobile': '?0',
  	  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
  	  'origin': 'https://www.dickssportinggoods.com',
   	 'sec-fetch-site': 'same-site',
  	  'sec-fetch-mode': 'cors',
    	'sec-fetch-dest': 'empty',
   	 'referer': link ,
  	  'accept-language': 'en-US,en;q=0.9',
		}

	params = (
	    ('location', "0"),
	    ('sku', sku),
	)

	response = requests.get('https://availability.dickssportinggoods.com/v1/inventoryapis/searchinventory', headers=headers, params=params)
	stock = json.loads(response.text)

	print(stock)
	if stock['status'] == 'OK':
		print("In stock, Starting Checkout")
		checkout()
		return
	else:
		print("Not In Stock, Remonitoring")
		check_stock()

check_stock()


class checkout():
	def __init__(self):
		pass
