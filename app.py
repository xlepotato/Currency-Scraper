import os
from flask import Flask
from flask import request, jsonify
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

app = Flask(__name__)
app.config["DEBUG"] = True

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "/usr/bin/google-chrome"
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--headless") # run chrome on headless mode, no window GUI while scraping



'''
    Function for testing during deployment
'''
@app.route('/')
def hello_world():
    return '''
           <html>
               <body>
                    <h1>Welcome to CurrencyScraper API!</h1>
                    <p> To retrieve all available money changer data (total of 212 iteration), send a HTTP GET request to: <font color="#005c99"> /api/v1/resources/moneychanger/details </font> </p>
                    <p> To iterate through 20 different money changer (for testing purposes only), send a HTTP GET request to: <font color="#005c99"> /api/v1/resources/moneychanger/test </font> </p>
                    <div style="position:fixed;bottom:0;height:auto;margin-top:40px;width:100%">Currency Web API created by Team Anything with love.</div>
               </body>
           </html>
       '''


'''
    Function to display all the best rate of different currencies with respect to SGD
'''
@app.route('/api/v1/resources/currency/buy/bestrate/all', methods=['GET'])
def buy_bestrate():
    URL = "https://cashchanger.co/singapore"
    try:
        r = requests.get(URL)
    except:
        print("An error occured.")
    soup = BeautifulSoup(r.content, 'html.parser')
    best_rate_container = soup.find('div', class_='container bestrate-container')
    currencies = []

    for row in best_rate_container.find_all('div', class_='bestrate'):
        print(row.prettify)
        currency = {}
        currency['country_currency'] = row.find('span', class_='country-currency').text
        currency['currency_code'] = row.find('span', class_='currency-code float-left').text
        currency['rate'] = row.find('div', class_='text-big text-center').text
        currencies.append(currency)

    return jsonify(currencies)


@app.route('/api/v1/resources/moneychanger/profile', methods=['GET']) # Get a specific money changer info for testing purposes
def get_profile():
    MONEYCHANGER_URL = "https://cashchanger.co/singapore/mc/simlim-exchange-and-trading/189"
    try:
        r = requests.get(MONEYCHANGER_URL)
    except:
        print("An error occured.")
    soup = BeautifulSoup(r.content, 'html.parser')
    profile = soup.find('div', class_='mc-detail')
    details = []
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
        details.append(detail)
    return jsonify(details)




@app.route('/api/v1/resources/moneychanger/details', methods=['GET'])
def get_moneychanger():
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=chrome_options) # Use the chromedriver installed
    # driver = webdriver.Chrome(r'C:\Users\WNG056\Downloads\chromedriver_win32\chromedriver.exe') # Uncomment for localhost testing
    details = []

    for i in range(1, 212):
        driver.get('https://cashchanger.co/singapore/mc/firman-hah-international-exchange/' + str(i))
        mc_detail = driver.find_elements_by_class_name('mc-detail')
        detail = {}
        try:
            detail['img'] = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[2]/div[1]/section[2]/div/div[1]/div/div/div[1]/img').get_attribute(
                'src')  # get the img src
        except:
            continue
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
                        if inverse_rate[1].text != '':  # check if the rate display info for sell is available
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
                        if inverse_rate[1].text != '':  # check if the rate display info for sell is available
                            currency['rate_sell'] = col[5]
                            currency['last_update_sell'] = col[6]
                        else:  # rate display info for sell is missing
                            currency['rate_sell'] = '-'
                            currency['last_update_sell'] = col[5]
                    currencies.append(
                        currency)  # append all the available currencies offered by a particular money changer to a list
            detail['currency_table'] = currencies
            details.append(detail)
        except Exception as e:
            print(e)
            pass  # skip the page if the relevant info of the money changer is not available to scrape
    for k in details:
        print(k)
    print(len(details))  # print the length of the data scrapped
    return jsonify(details)  # return the data in json format


'''
    Function used for testing purposes in replace with the original function.
    Only Iterate up to 20 different Money Changer web pages.
'''

@app.route('/api/v1/resources/moneychanger/test', methods=['GET'])
def get_moneychanger_test():
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=chrome_options)  # Use the chromedriver installed
    # driver = webdriver.Chrome(r'C:\Users\WNG056\Downloads\chromedriver_win32\chromedriver.exe') # Uncomment for localhost testing
    details = []

    for i in range(1, 21):
        driver.get('https://cashchanger.co/singapore/mc/firman-hah-international-exchange/' + str(i))
        mc_detail = driver.find_elements_by_class_name('mc-detail')
        detail = {}
        try:
            detail['img'] = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[2]/div[1]/section[2]/div/div[1]/div/div/div[1]/img').get_attribute(
                'src')  # get the img src
        except:
            continue
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
                        if inverse_rate[1].text != '':  # check if the rate display info for sell is available
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
                        if inverse_rate[1].text != '':  # check if the rate display info for sell is available
                            currency['rate_sell'] = col[5]
                            currency['last_update_sell'] = col[6]
                        else:  # rate display info for sell is missing
                            currency['rate_sell'] = '-'
                            currency['last_update_sell'] = col[5]
                    currencies.append(
                        currency)  # append all the available currencies offered by a particular money changer to a list
            detail['currency_table'] = currencies
            details.append(detail)
        except Exception as e:
            print(e)
            pass  # skip the page if the relevant info of the money changer is not available to scrape
    for k in details:
        print(k)
    print(len(details))  # print the length of the data scrapped
    return jsonify(details)  # return the data in json format


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))
