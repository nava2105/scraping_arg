from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

while True:

    url = 'https://es.investing.com/currencies/usd-ars'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Value of a dollar in argentinian pound
    val = soup.find_all('div', class_='text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]')
    # print(val)
    # Change rate
    chan = soup.find_all('div', class_='flex items-center gap-2 text-base/6 font-bold md:text-xl/7 rtl:force-ltr text-positive-main')
    # print(chan)

    value = list()
    for i in val:
        value.append(i.text)
        for j in chan:
            value.append(j.text)
    print(value)
    time.sleep(10)
