from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
import threading
import psycopg2
from psycopg2 import sql, Error

conn_params = {
    "dbname": "localhost",
    "user": "postgres",
    "password": "Mmnsin210606?",
    "host": "localhost",
    "port": "5432"
}

try:
    # Connect to the database
    conn = psycopg2.connect(**conn_params)
    print("Successful connection")
except Error:
    print("Failed connection")

exchange = list()
risk = list()

def exchange_scraper():
    try:
        # Connect to the database
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS arg_exchange
            (
                date date NOT NULL,
                "time" time without time zone NOT NULL,
                value numeric NOT NULL,
                variance real,
                variance_percentage real
            )""")
        print("Successful connection")
        while True:
            url1 = 'https://es.investing.com/currencies/usd-ars'
            page1 = requests.get(url1)
            soup1 = BeautifulSoup(page1.content, 'html.parser')

            # Value of a dollar in argentinian pound
            val = soup1.find_all('div', class_='text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]')
            # print(val)
            # Variation
            chan = soup1.find_all('div',
                                  class_='flex items-center gap-2 text-base/6 font-bold md:text-xl/7 rtl:force-ltr text-positive-main')
            # print(chan)

            exchange.append(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
            date = datetime.now().date()
            moment = datetime.now().strftime('%H:%M:%S')
            for i in val:
                exchange.append(i.text)
                value = float(i.text.replace(',','.'))
            var = False
            for i in chan:
                if i.text != None:
                    exchange.append(i.text)
                    percent = float(i.text[9:12].replace(',','.'))
                    variance = float(i.text[1:6].replace(',','.'))
                    var = True
            if var:
                print(exchange[-3] + " | " + exchange[-2] + " | " + exchange[-1])
                cursor.execute("""INSERT INTO arg_exchange
                                (date, time, value, variance, variance_percentage) 
                                VALUES (%s, %s, %s, %s, %s)""", (date, moment, value, variance, percent))
                cursor.execute("SELECT * FROM arg_exchange")
                conn.commit()
            else:
                print(exchange[-2] + " | " + exchange[-1])
            time.sleep(9)
    except Error as e:
        print(e)

def risk_scraper():
    try:
        # Connect to the database
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS arg_risk
            (
                "date" date NOT NULL,
                "time" time without time zone NOT NULL,
                "last_value" numeric,
                "variance" real
            )""")
        print("Successful connection")
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
            date = datetime.now().date()
            moment = datetime.now().strftime('%H:%M:%S')
            for i in rsk:
                risk.append(i.text)
                value = float(i.text.replace(',', '.'))
            for i in crv:
                risk.append(i.text)
                variance = float(i.text[1:4].replace(',', '.'))
            print(risk[-3] + " | " + risk[-2] + " | " + risk[-1])
            cursor.execute("""INSERT INTO arg_risk
                            (date, time, last_value, variance)
                            VALUES (%s, %s, %s, %s)""", (date, moment, value, variance))
            cursor.execute("SELECT * FROM arg_risk")
            conn.commit()
            time.sleep(28800)
    except Error as e:
        print(e)

hilo1 = threading.Thread(target=exchange_scraper)
hilo2 = threading.Thread(target=risk_scraper)

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()