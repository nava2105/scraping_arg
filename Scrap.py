from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
import threading

exchange = list()
risk = list()

def exchange_scraper():
    while True:
        url1 = 'https://es.investing.com/currencies/usd-ars'
        page1 = requests.get(url1)
        soup1 = BeautifulSoup(page1.content, 'html.parser')

        # Value of a dollar in argentinian pound
        val = soup1.find_all('div', class_='text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]')
        # print(val)
        # Variation
        chan = soup1.find_all('div', class_='flex items-center gap-2 text-base/6 font-bold md:text-xl/7 rtl:force-ltr text-positive-main')
        # print(chan)
        exchange.append(datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
        for i in val:
            exchange.append(i.text)
        var = False
        for i in chan:
            if i.text != None:
                exchange.append(i.text)
                var = True
        if var:
            print(exchange[-3] + " | " + exchange[-2] + " | " + exchange[-1])
        else:
            print(exchange[-2] + " | " + exchange[-1])
        time.sleep(9)

def risk_scraper():
    while True:
        driver = webdriver.Edge()
        driver.get('https://www.ambito.com/contenidos/riesgo-pais.html')
        html = driver.page_source
        soup2 = BeautifulSoup(html, 'html.parser')

        # Country risk
        rsk = soup2.find_all('span', class_='day-summary__value value data-valor')
        # print(rsk)
        # Country risk
        crv = soup2.find_all('span', class_='variation-last__percent percent data-class-variacion data-variacion indicators__value down')
        # print(crv)
        risk.append(datetime.now().strftime('%d.%m.%Y'))
        for i in rsk:
            risk.append(i.text)
        for i in crv:
            risk.append(i.text)
        try:
            print(risk[-3] + " | " + risk[-2] + " | " + risk[-1])
        except IndexError:
            print(risk[-2] + " | " + risk[-1])
        time.sleep(28800)

hilo1 = threading.Thread(target=exchange_scraper)
hilo2 = threading.Thread(target=risk_scraper)

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()