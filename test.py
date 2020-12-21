from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time



def getCookies(url):
    PROXY = "socks5://p.webshare.io:9999"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)

    PATH = 'C:\Program Files (x86)\chromedriver.exe'

    driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

    driver.get(url)

    bm_sz = driver.get_cookie('bm_sz')['value']
    UID = driver.get_cookie('UID')['value']
    pst2 = driver.get_cookie('pst2')['value']
    physical_dma = driver.get_cookie('physical_dma')['value']
    customerZipCode = driver.get_cookie('customerZipCode')['value']
    vt = driver.get_cookie('vt')['value']
    oid = driver.get_cookie('oid')['value']
    abck = driver.get_cookie('_abck')['value']
    CTT = driver.get_cookie('CTT')['value']
    SID = driver.get_cookie('SID')['value']

    driver.close()


    return bm_sz, UID, pst2, physical_dma, customerZipCode, vt, oid, abck, CTT, SID
