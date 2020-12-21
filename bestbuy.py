from base64 import b64encode

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


import requests
import json
import time
import test

class checkout():

    def __init__(self):
        self.link = 'https://www.bestbuy.com/site/apple-airpods-with-wireless-charging-case-latest-model-white/6083595.p?skuId=6083595'  #Enter the link from Bestbuy
        self.skuId = self.link[len(self.link) - 7:len(self.link)]  #Gets SkuID from the last 7 digits of the link
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.inStock = False
        self.country = 'US'
        self.firstName = 'Joe'
        self.lastName = 'Mama'
        self.street = ''
        self.city = 'N'
        self.zipCode = ''
        self.state = ''  #EX: NY
        self.phoneNum = ''
        self.cardNum = ''
        self.cardType = ''
        self.cvv = ''
        self.month = ''
        self.year = ''
        self.bm_sz, self.UID, self.pst2, self.physical_dma, self.customerZipCode, self.vt, self.oid, self.abck, self.CTT, self.SID = test.getCookies(self.link)
        self.get_tas_data()
        self.checkStock()

    def get_tas_data(self):

        headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                "content-type": "application/json",
                "user-agent": "Mozilla/5.0"
            }

        r = requests.get("https://www.bestbuy.com/api/csiservice/v2/key/tas", headers=headers)
        key = json.loads(r.text)['publicKey']
        keyId = json.loads(r.text)['keyId']
        key = RSA.importKey(key)
        cipher = PKCS1_OAEP.new(key)
        encrypted_card = b64encode(cipher.encrypt(("00926999" + self.cardNum).encode("utf-8"))).decode("utf-8")
        zero_string = ""
        for i in range(len(self.cardNum) - 10):
            zero_string += "0"
        self.bin_number = self.cardNum[:6]
        encrypted_card += ":3:" + keyId + ":" + self.bin_number + zero_string + self.cardNum[-4:]
        self.encrypted_card = encrypted_card



    def checkStock(self):
        i = 0
        while self.inStock == False:

            headers = {'User-Agent': 'Mozilla/5.0'}

            r = requests.get(self.link, headers=headers)

            jsons = json.loads(r.text.split("initializer.initializeComponent(")[1].split("""", 'en-US');""")[0].replace("\\", "")[162:])

            buttonState = jsons['app']['buttonState']
            availability = jsons['app']["availability"]

            if buttonState and availability > 0:
                print('InStock')
                self.inStock == True

                self.add_to_cart()


                return self.inStock

            else:
                print("Not In stock")
                time.sleep(1)



    def add_to_cart(self):
        cookies1 = {
            '52245': '',
            'UID': self.UID,
            'pst2': self.pst2,
            'physical_dma': self.physical_dma,
            'customerZipCode': self.customerZipCode,
            'ltc': '%20',
            'oid': self.oid,
            'vt': self.vt,
            'bm_sz': self.bm_sz,
            '_abck': self.abck,
            'CTT': self.CTT,
            'SID': self.SID
        }

        self.headers = {
            'authority': 'www.bestbuy.com',
            'accept': 'application/json',
            'User-Agent': 'Mozilla/5.0',
            'content-type': 'application/json; charset=UTF-8',
            'origin': 'https://www.bestbuy.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.link,
            'accept-language': 'en-US,en;q=0.9',

        }

        data = {"items":[{"skuId":self.skuId}]}
        self.s = requests.Session()
        response = self.s.post('https://www.bestbuy.com/cart/api/v1/addToCart', headers=self.headers, json=data, cookies=cookies1, timeout=10)
        jsondata = json.loads(response.text)
        cartCount = jsondata["cartCount"]
        try:
            self.orderId = jsondata['summaryItems'][1]['lineId']
        except:
            print(jsondata)
        print(self.orderId)


        if response.status_code == 200 and cartCount == 1:
            print("Added to cart")
            self.shipping()
        else:
            print("Add to cart Failed Retrying ")
            self.add_to_cart()




    def shipping(self):

        data = {"country":"US","saveToProfile":'false',"street2":"","useAddressAsBilling":'true',"middleInitial":"","lastName":self.lastName,"street":self.street,"isWishListAddress":'false',"city":self.city,"override":'false',"zipcode":self.zipCode,"state":self.state,"dayPhoneNumber":self.phoneNum,"firstName":self.firstName}
        headers = {
            'authority': 'www.bestbuy.com',
            'accept': 'application/json',
            'User-Agent': 'Mozilla/5.0',
            'content-type': 'application/json; charset=UTF-8',
            'origin': 'https://www.bestbuy.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.bestbuy.com/checkout/r/payment',
            'accept-language': 'en-US,en;q=0.9',
            'path': '/checkout/standardizeAddress'

        }


        r = self.s.post('https://www.bestbuy.com/checkout/standardizeAddress', json=data, headers=headers)
        if r.status_code == 200:
            print('Added Shipping Details')
            self.billing()

        else:
            print("Submitting Shpping failed. Retrying")
            self.shipping()






    def billing(self):

        headers = {
            "accept": "application/com.bestbuy.order+json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "content-type": "application/json",
            "origin": "https://www.bestbuy.com",
            "referer": "https://www.bestbuy.com/checkout/r/fulfillment",
            "user-agent": "Mozilla/5.0",
            "x-user-interface": "DotCom-Optimized"
        }
                #Billing Info
        body = {"billingAddress": {
            "country": "US",
            "saveToProfile": False,
            "street2":"self.lastName",
            "useAddressAsBilling": True,
            "middleInitial": "",
            "lastName":self.lastName,
            "street": self.street,
            "city": self.city,
            "override": False,
            "zipcode": self.zipCode,
            "state": self.state,
            "dayPhoneNumber": self.phoneNum,
            "firstName": self.firstName,
            "isWishListAddress": False},
            "creditCard": {
                "hasCID": False,
                "invalidCard": False,
                "isCustomerCard": False,
                "isNewCard": True,
                "isVisaCheckout": False,
                "govPurchaseCard": False,
                "isInternationalCard": False,
                "number": self.encrypted_card,
                "binNumber": self.bin_number,
                "cardType": self.cardType,
                "cid": self.cvv,
                "expiration": {"month": self.month, "year": self.year},
                "isPWPRegistered": False}}

        response = self.s.put(f'https://www.bestbuy.com/payment/api/v1/payment/{self.orderId}/creditCard',
                              headers=headers, data=body)
        print(response.text)

        r = json.loads(response.text)


        print(response.status_code)

        if response.status_code == 200:
            print("Checkout Succesful")
        else:
            print("Checkout Failed Retrying")
            self.checkStock()
            time.sleep(3)


checkout()
