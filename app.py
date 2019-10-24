import os
from flask import Flask
from flask import request, jsonify
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

app = Flask(__name__)
app.config["DEBUG"] = True

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--headless")

URL = "https://cashchanger.co/singapore"

@app.route('/')
def hello_world():
    MONEYCHANGER_URL = "https://cashchanger.co/singapore/mc/simlim-exchange-and-trading/189"
    try:
        r = requests.get(MONEYCHANGER_URL)
    except:
        print("An error occured.")
        # soup = BeautifulSoup(page, 'html.parser')
    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify) # gives the visual representation of the parse tree created from the raw HTML content.
    profile = soup.find('div', class_='mc-detail')
    # print(profile.prettify)
    details = []

    # bestrate_table = best_rate_container.find_all('div', class_='bestrate')
    for row in profile.find_all('div', class_='profile-card box'):
        print(row.prettify)
        detail = {}
        detail['name'] = row.find('h1', class_='text-black').text
        detail['operating_hours'] = row.find('p', class_='js-intro-openinghours-container').text
        detail['tel_No'] = row.find('p', class_='js-intro-mc-phone-container contact').a['href']
        detail['mrt'] = row.find_all('p')[2].text
        detail['address'] = row.find('p', class_='js-intro-mc-address-container').text

        # Clean data
        detail['mrt'] = (detail['mrt'].replace("\n", "")).strip()
        detail['address'] = (detail['address'].replace("\n", "")).strip().partition("      ")[0]
        detail['operating_hours'] = (detail['operating_hours'].replace("\n", "")).strip().replace("  ", "")
        # .replace("  ","")

        details.append(detail)
    # print(bestrate_table.prettify)
    return jsonify(details)


@app.route('/api/v1/resources/currency/bestrate/all', methods=['GET'])
def api_bestrate():
    try:
        # page = urllib.request.urlopen(url) # conntect to website
        r = requests.get(URL)
    except:
        print("An error occured.")
        # soup = BeautifulSoup(page, 'html.parser')
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup.prettify) # gives the visual representation of the parse tree created from the raw HTML content.
    best_rate_container = soup.find('div', class_='container bestrate-container')
    print(best_rate_container.prettify)


    # regex = re.compile('^tocsection-')
    #     # content_lis = soup.find_all('li', attrs={'class': regex})
    #     # print(content_lis)
    #     # content = []
    #     # for li in content_lis:
    #     #     content.append(li.getText().split('\n')[0])
    #     # print(content)
    #     # return jsonify(content)
    return 'nyan'

    # # Getting the keywords section
    # keyword_section = soup.find(class_="keywords-section")
    # # Same as: soup.select("div.article-wrapper grid row div.keywords-section")
    #
    # # Getting a list of all keywords which are inserted into a keywords list in line 7.
    # keywords_raw = keyword_section.find_all(class_="keyword")
    # keyword_list = [word.get_text() for word in keywords_raw]


@app.route('/api/v1/resources/currency/buy/bestrate/all', methods=['GET'])
def buy_bestrate():
    try:
        # page = urllib.request.urlopen(url) # conntect to website
        r = requests.get(URL)
    except:
        print("An error occured.")
        # soup = BeautifulSoup(page, 'html.parser')
    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify) # gives the visual representation of the parse tree created from the raw HTML content.
    best_rate_container = soup.find('div', class_='container bestrate-container')
    # print(best_rate_container.prettify)
    currencies = []

    # bestrate_table = best_rate_container.find_all('div', class_='bestrate')
    for row in best_rate_container.find_all('div', class_='bestrate'):
        print(row.prettify)
        currency = {}
        currency['country_currency'] = row.find('span', class_='country-currency').text
        currency['currency_code'] = row.find('span', class_='currency-code float-left').text
        currency['rate'] = row.find('div', class_='text-big text-center').text
        currencies.append(currency)
    # print(bestrate_table.prettify)


    # regex = re.compile('^tocsection-')
    #     # content_lis = soup.find_all('li', attrs={'class': regex})
    #     # print(content_lis)
    #     # content = []
    #     # for li in content_lis:
    #     #     content.append(li.getText().split('\n')[0])
    #     # print(content)
    #     # return jsonify(content)
    return jsonify(currencies)
    # return 'nyan'

    # # Getting the keywords section
    # keyword_section = soup.find(class_="keywords-section")
    # # Same as: soup.select("div.article-wrapper grid row div.keywords-section")
    #
    # # Getting a list of all keywords which are inserted into a keywords list in line 7.
    # keywords_raw = keyword_section.find_all(class_="keyword")
    # keyword_list = [word.get_text() for word in keywords_raw]


@app.route('/api/v1/resources/moneychanger/profile', methods=['GET'])
def get_profile():
    MONEYCHANGER_URL = "https://cashchanger.co/singapore/mc/simlim-exchange-and-trading/189"
    try:
        r = requests.get(MONEYCHANGER_URL)
    except:
        print("An error occured.")
        # soup = BeautifulSoup(page, 'html.parser')
    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify) # gives the visual representation of the parse tree created from the raw HTML content.
    profile = soup.find('div', class_='mc-detail')
    # print(profile.prettify)
    details = []

    # bestrate_table = best_rate_container.find_all('div', class_='bestrate')
    for row in profile.find_all('div', class_='profile-card box'):
        print(row.prettify)
        detail = {}
        detail['name'] = row.find('h1', class_='text-black').text
        detail['operating_hours'] = row.find('p', class_='js-intro-openinghours-container').text
        detail['tel_No'] = row.find('p', class_='js-intro-mc-phone-container contact').a['href']
        detail['mrt'] = row.find_all('p')[2].text
        detail['address'] = row.find('p', class_='js-intro-mc-address-container').text

        # Clean data
        detail['mrt'] = (detail['mrt'].replace("\n", "")).strip()
        detail['address'] = (detail['address'].replace("\n", "")).strip().partition("      ")[0]
        detail['operating_hours'] = (detail['operating_hours'].replace("\n", "")).strip().replace("  ", "")
        # .replace("  ","")

        details.append(detail)
    # print(bestrate_table.prettify)
    return jsonify(details)




@app.route('/api/v1/resources/moneychanger/moneychanger', methods=['GET'])
def get_moneychanger():
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # driver = webdriver.Chrome(r'C:\Users\WNG056\Downloads\chromedriver_win32\chromedriver.exe')
    details = []

    for i in range(1,6):
        driver.get('https://cashchanger.co/singapore/mc/firman-hah-international-exchange/' + str(i))
        mc_detail = driver.find_elements_by_class_name('mc-detail')
        detail = {}
        # try:
        #     detail['img'] = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/section[2]/div/div[1]/div/div/div[1]/img').get_attribute('src')  # get the img src
        # except:
        #     continue
        for row in mc_detail:
            currencies = []
            col = row.text.split('\n')
            if col[0] != '':  # check if there is empty data
                try:
                    # if operating hours info is available
                    driver.find_element_by_class_name('js-intro-openinghours-container')
                    detail['moneychanger_name'] = col[0]
                    detail['operating_hours'] = col[1]
                    detail['tel_No'] = col[2]
                    detail['mrt'] = col[3]
                    detail['address'] = col[4]
                except:
                    # if operating hours info is unavailable
                    detail['moneychanger_name'] = col[0]
                    detail['operating_hours'] = '-'
                    detail['tel_No'] = col[1]
                    detail['mrt'] = col[2]
                    detail['address'] = col[3]
        try:
            currency_table = driver.find_element_by_class_name('mc-currencyratetable')
            currency_data = currency_table.find_elements_by_class_name(' currencybox-rate')
            for row in currency_data:
                currency = {}
                col = row.text.split('\n')
                if col[0] != '':
                    inverse_rate = row.find_elements_by_class_name('inverserate')
                    if inverse_rate[0].text != '':  # check if the rate display info for buy is available
                        currency['currency_code'] = col[0]
                        currency['currency_name'] = col[1]
                        currency['exchange_rate_buy'] = col[2]
                        currency['rate_buy'] = col[3]
                        currency['last_update_buy'] = col[4]
                        currency['exchange_rate_sell'] = col[5]
                        if inverse_rate[1].text != '': # check if the rate display info for sell is available
                            currency['rate_sell'] = col[6]
                            currency['last_update_sell'] = col[7]
                        else:  # rate display info for sell is missing
                            currency['rate_sell'] = '-'
                            currency['last_update_sell'] = col[6]
                    else:  # rate display info for buy is missing
                        currency['currency_code'] = col[0]
                        currency['currency_name'] = col[1]
                        currency['exchange_rate_buy'] = col[2]
                        currency['rate_buy'] = '-'
                        currency['last_update_buy'] = col[3]
                        currency['exchange_rate_sell'] = col[4]
                        if inverse_rate[1].text != '':   # check if the rate display info for sell is available
                            currency['rate_sell'] = col[5]
                            currency['last_update_sell'] = col[6]
                        else: # rate display info for sell is missing
                            currency['rate_sell'] = '-'
                            currency['last_update_sell'] = col[5]
                    currencies.append(currency)  # append all the available currencies offered by a particular money changer to a list
            detail['currency_table'] = currencies
            details.append(detail)
        except Exception as e:
            print(e)
            pass  # skip the page if the relevant info of the money changer is not available to scrape
    for k in details:
        print(k)
    print(len(details)) # print the length of the data scrapped
    return jsonify(details)  # return the data in json format



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))
