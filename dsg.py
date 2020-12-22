import requests
import json
import random
import time

class checkout():
	def __init__(self):
		self.s = requests.Session()
		self.sku = '21861756'
		self.add_to_cart()
		

	def add_to_cart(self):
		
		self.link = 'https://www.dickssportinggoods.com/p/breakingt-mens-mookie-of-the-year-grey-t-shirt-20wqtmmlbddgrsgrylada/20wqtmmlbddgrsgrylada'
		sku = '21861756'

		headers = {
		    'authority': 'www.dickssportinggoods.com',
		    'content-length': '0',
		    'x-instana-t': 'e65a4ae6e1205eab',
		    'accept': '*/*',
		    'x-instana-s': 'e65a4ae6e1205eab',
		    'sec-ch-ua-mobile': '?0',
		    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
		    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
		    'x-instana-l': '1,correlationType=web;correlationId=e65a4ae6e1205eab',
		    'origin': 'https://www.dickssportinggoods.com',
		    'sec-fetch-site': 'same-origin',
		    'sec-fetch-mode': 'cors',
		    'sec-fetch-dest': 'empty',
		    'referer': self.link, 
		    'accept-language': 'en-US,en;q=0.9'}

		params = (
		    ('qty', '1'),
		)

		r = requests.put('https://www.dickssportinggoods.com/api/v1/carts/contents/' + sku, headers=headers, params=params)

		inCart = r.text
		print(inCart)
		if inCart == sku:
			print("Added To cart, Sumbming Cart")
			self.submit_cart()
		else:
			print("Adding To Cart Failed Retrying")
			print(r.text)

	def submit_cart(self):


		
		headers = {
		    'authority': 'www.dickssportinggoods.com',
		    'sec-ch-ua-mobile': '?0',
		    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
		    
		    'accept': 'application/json',
		    
		    'content-type': 'application/json',
		    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
		    'origin': 'https://www.dickssportinggoods.com',
		    'sec-fetch-site': 'same-origin',
		    'sec-fetch-mode': 'cors',
		    'sec-fetch-dest': 'empty',
		    'referer': 'https://www.dickssportinggoods.com/p/horizon-fitness-t101-treadmill-18hrzut101trdmllxtrd/18hrzut101trdmllxtrd?recid=cartempty_PageElement_cartempty_rr_1_34473_&rrec=true',
		    'accept-language': 'en-US,en;q=0.9',
		}

		data = {"level":"LOG","message":{"callOrigin":"PDP main button","success":"true","skuId":self.sku,"quantity":1,"chain":"dsg"}}

		response = self.s.post('https://www.dickssportinggoods.com/p/spring/msvc/logger/publish', headers=headers, json=data)
		jsons = json.loads(response.text)
		if jsons['status'] == 'true':
			print("Added To cart going to checkout")
		else:
			print("Error Adding To Cart, Remonitoring")
			check_stock()

		

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
  	  'accept-language': 'en-US,en;q=0.9'}

	params = (
	    ('location', '0'),
	    ('sku', sku),
	)

	response = requests.get('https://availability.dickssportinggoods.com/v1/inventoryapis/searchinventory', headers=headers, params=params)
	try:
		stock = json.loads(response.text)
	finally:
		print(response.text)

	
	if stock['status'] == 'OK':
		print("In stock, Starting Checkout")
		cookies = response.cookies
		checkout()
		return 

	else:
		print("Not In Stock, Remonitoring")
check_stock()

		




