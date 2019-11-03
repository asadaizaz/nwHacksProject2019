from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import  Options
import csv
import os
import config
from datetime import date
from bs4 import BeautifulSoup
import pickle
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#Asad Aizaz; Jan 26 2019
#Test
# Returns a Array[Column][Row] with all the information
# from the data.csv file. Fixed 6 column, does not handle
# errors
def parseDataCSV():
    config.data = [[] for x in range(0,6)]
    with open('data.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            for x in range(0, 6):
                if (x == 3 or x == 2 or x == 4):
                    row[x] = float(row[x])
                elif (x == 0):
                    asList = row[x].split('-')
                    converted = list(map(lambda x: int(x), asList))
                    row[x] = date(converted[2], converted[1], converted[0])
                config.data[x].append(row[x])

# Returns a dictionary with name:(lat, long)
def parseLocationCSV():
    with open('location.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            config.locations[row[0]] = (float(row[1]), float(row[2]))


def formatDate(date):
    months = dict(JAN = "01", FEB="02", MAR="03", APR="04", MAY="05", JUN="06", JUL="07", AUG="08", SEP="09", OCT="10", NOV="11", DEC="12")
    s = date[:3] + months[date[3:6]] + date[6:]
    return s

def authenticateLogin():
    url = "https://secure.housing.ubc.ca/cas/sgw/cwl_auth.home"
    newUrl = ""
    chromeOP = Options()
    chromeOP.add_argument("--disable-infobars")

    #browser = webdriver.Remote(command_executor='http://127.0.0.1:5000/', desired_capabilities=DesiredCapabilities.CHROME)
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chromeOP)
    browser.set_window_size(400, 600)
    browser.set_window_position(0, 0)

    browser.get(url)
    while (newUrl != "https://secure.housing.ubc.ca/cas/sgw/cwl_auth.home"):
        newUrl = browser.current_url
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
    browser.close()
    start()
def parseTransactions(html):
    hack  = 1
    soup = BeautifulSoup(html, "html.parser")
    fieldnames = ['date', 'loc', 'lat', 'long', 'amt', 'card']
    date = ""
    amt = ""
    loc = ""
    with open("data.csv", mode='w') as csv_file:
        c = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for foo in soup.find_all('div', attrs={'class': ['row-highlight', '']}):
            fooD = foo.descendants
            # print("foo")
            for d in fooD:
                # print("d")
                if d.name == 'div' and d.get('class', '') == ['item-left']:
                    print(d.text)
                    date = formatDate(d.text)

                if d.name == 'div' and d.get("class", '') == ['item-right']:
                    print(d.text)
                    if d.text[1] == '-':
                        print(d.text[2:])
                        amt = d.text[2:]

                if d.name == 'div' and d.get("class", '') == ['item-comments']:
                    print(d.text)
                    loc = d.text.split("Location: ", 1)[1]
            if hack != 1:
              if config.locations.get(loc, (0,0)) is not (0,0):
                c.writerow({'date': date, 'amt': amt, 'loc': loc, 'lat': config.locations.get(loc, (0,0))[0],'long' : config.locations.get(loc, (0,0))[1], 'card': "UBC Card"})
            hack = 0
def start():
    chromeOP = Options()
    chromeOP.add_argument("--headless")
    browser = webdriver.Chrome(chrome_options=chromeOP)
    browser.get("https://secure.housing.ubc.ca/cas/sgw/ws_mpvan_plans.accounts?p_action=VIEW_ACCT")

    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.get("https://secure.housing.ubc.ca/cas/sgw/ws_mpvan_plans.accounts?p_action=VIEW_ACCT")

    browser.find_element_by_xpath(
        "/html/body/div[@class='container']/div[6]/div[@class='content expand']/div[@class='row-fluid expand']/p[5]/a[1]").click()
    dropDown = Select(browser.find_element_by_id("p_start_date"))
    dropDown.select_by_index(11)
    browser.find_element_by_name("SUBMIT").click()
    html = browser.page_source
    parseTransactions(html)

def main():
    parseLocationCSV()
    authenticateLogin()
#main()
