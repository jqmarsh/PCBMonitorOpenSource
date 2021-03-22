# Imports
from selenium import webdriver
import os
import random
import time
import ast
import urllib3
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType, OperatingSystem
import smtplib
import logging

def linespace():
    print(' ')


# Startup message
def program_start_message():
    linespace()
    print("""Welcome to the official PCB Monitor!
    Version: 0.2
    Check us out on PCBot.cooking for more info!""")
    linespace()


# Config File
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
Driver_Path = os.path.join(ROOT_DIR, 'chromedriver')


# Headers to disguise us, or at least try
software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.COMPUTER]
operating_systems = [OperatingSystem.WINDOWS.value]
user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type, operating_systems=operating_systems)


# Monitor Start Message
program_start_message()

# Store Selector
StoreList = []
Store = input('Please input the store you would like to monitor (e.g. Amazon, Walmart, Target, Bestbuy, Pokemon Center, or Pokemon Center Japan): ')
linespace()
StoreList.append(Store)
print('Your Selected Store: ' + str(Store))
linespace()

#Multiple Stores At Once
"""while True:
    storecheck = input('Would you like to monitor another store/item [y/n]?: ')
    func.linespace()
    if storecheck == "n":
        break
    elif storecheck == "y":
        Store2 = input('Please input the store you would like to monitor (e.g. Amazon, Walmart, Target, Bestbuy, Pokemon Center): ')
        func.linespace()
        StoreList.append(Store2)
        continue
for string in StoreList:
    print("Starting " + string + " Monitor(s)!")
func.linespace()"""

# Product Page URL Selector
input_url = input('Please input the product page URL: ')
linespace()
print('Your Input URL: ' + input_url)
linespace()


# Humanizes The Monitor
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument("--start-maximized")
option.add_argument("window-size=1920,1080")
option.add_argument("disable-infobars")
option.add_argument("--lang=es")
option.add_argument("--disable-plugins-discovery")
option.add_argument("--incognito")
option.add_argument('--profile-directory=Default')
option.add_argument("--log-level=3")
option.add_argument("--disable-dev-shm-usage")
option.add_argument("--no-sandbox")


# Debugging
DEBUG = False
DebugCheck = input("Would you like to enable Debugging? [y/n]: ")
linespace()
if DebugCheck == "y":
    DEBUG = True
    print("Debugging has been enabled")
    linespace()
    logging.basicConfig(filename='PCBMonitorLog.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s',
                        level=logging.DEBUG)
else:
    DEBUG = False
    option.add_argument("--headless")

def send_email(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # start smtp server on port 587
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)  # login to gmail server
        server.sendmail(FROM, TO, message)  # actually perform sending of mail
        server.close()  # end server
        print('Successfully sent the email restock notification!')  # alert user mail was sent
    except Exception as e:  # else tell user it failed and why (exception e)
        print("Failed to send email! Check the email you entered and verify it's correct. " + str(e))


# PokemonCenter.Com Monitor
def pokemoncentermonitor():
    print("Please Note: Residential Proxies Are Highly Recommended. Otherwise, Don't Use A Proxy. Not Using Residential Proxies May Result In Captchas")
    linespace()
    proxyChecker = input("Would you like to use proxies? (Residential Proxies Only)[y/n]: ")
    linespace()
    loop = 0
    body = str(input_url) + ' IS BACK IN STOCK!'
    user = 'JqMarshBooking@gmail.com'
    pwd = 'kase cdsw cifl idsd'
    recipient = input("Please Enter The Email Address Where You Would Like Notifications Sent To: ")
    subject = "Your Monitored Item @ " + str(Store) + " Is Back In Stock"
    while True:
        global options
        if proxyChecker == "y":
            PROXY = [""]
            save_file = 'proxy_list.txt'
            if os.path.exists(save_file):
                with open(save_file) as f:
                    PROXY = ast.literal_eval(f.read())
            PROXY = random.choice(PROXY)
            print("Proxy Selected: " + PROXY)
            option.add_argument('--proxy-server=%s' % (PROXY))
        elif proxyChecker == "n":
            print("Monitoring without proxies.")
            linespace()
        else:
            print("Invalid Input. Please enter \'y\' or \'n\'.")
            linespace()
            continue
        userAgent = user_agent_rotator.get_random_user_agent()
        option.add_argument(f'user-agent={userAgent}')
        browser = webdriver.Chrome(executable_path=Driver_Path, options=option)
        linespace()
        browser.delete_all_cookies()
        browser.get("https://google.com")
        time.sleep(random.randint(1, 2))
        try:
            browser.get(input_url)
            addtocart = browser.find_element_by_class_name('_2Vyo6t5xf0vISrGJtN0OKA')
            if addtocart:
                print("Restock Detected")
                linespace()
                send_email(user, pwd, recipient, subject, body)
        except:
            loop += 1
            print("(Potentially) No Restock Detected. Are you using Residential Proxies? Use residential proxies or restart without proxies." )
            linespace()
            if loop >= 1:
                print("No Restock Detected.")
            linespace()
        finally:
            browser.quit()
            time.sleep(random.randint(60, 120))
            linespace()


# PokemonCenter.Com Monitor
def pokemoncentermonitorjpn():
    print("Please Note: Residential Proxies Are Highly Recommended. Otherwise, Don't Use A Proxy. Not Using Residential Proxies May Result In Captchas")
    linespace()
    proxyChecker = input("Would you like to use proxies? (Residential Proxies Only)[y/n]: ")
    linespace()
    loop = 0
    body = str(input_url) + ' IS BACK IN STOCK!'
    user = 'JqMarshBooking@gmail.com'
    pwd = 'kase cdsw cifl idsd'
    recipient = input("Please Enter The Email Address Where You Would Like Notifications Sent To: ")
    subject = "Your Monitored Item @ " + str(Store) + " Is Back In Stock"
    while True:
        global options
        if proxyChecker == "y":
            PROXY = [""]
            save_file = 'proxy_list.txt'
            if os.path.exists(save_file):
                with open(save_file) as f:
                    PROXY = ast.literal_eval(f.read())
            PROXY = random.choice(PROXY)
            print("Proxy Selected: " + PROXY)
            option.add_argument('--proxy-server=%s' % (PROXY))
        elif proxyChecker == "n":
            print("Monitoring without proxies.")
            linespace()
        else:
            print("Invalid Input. Please enter \'y\' or \'n\'.")
            linespace()
            continue
        userAgent = user_agent_rotator.get_random_user_agent()
        option.add_argument(f'user-agent={userAgent}')
        browser = webdriver.Chrome(executable_path=Driver_Path, options=option)
        linespace()
        browser.delete_all_cookies()
        browser.get("https://google.com")
        time.sleep(random.randint(1, 2))
        try:
            browser.get(input_url)
            addtocart = browser.find_element_by_class_name('add_cart_btn')
            if addtocart:
                print("Restock Detected")
                linespace()
                send_email(user, pwd, recipient, subject, body)
        except:
            loop += 1
            print("(Potentially) No Restock Detected. Are you using Residential Proxies? Use residential proxies or restart without proxies." )
            linespace()
            if loop >= 1:
                print("No Restock Detected.")
            linespace()
        finally:
            browser.quit()
            time.sleep(random.randint(60, 120))
            linespace()

# Amazon.com Monitor
def amazonmonitor():
    proxyChecker = input("Would you like to use proxies? (Residential Proxies Only) - If you start getting errors; restart the program without using proxies. [y/n]: ")
    linespace()
    msrpCheck = input("Please enter the MSRP of the product you're monitoring (e.g. $59.99): ")
    linespace()
    print("Input MSRP: " + str(msrpCheck))
    linespace()
    body = str(input_url) + ' IS BACK IN STOCK!'
    user = 'JqMarshBooking@gmail.com'
    pwd = 'kase cdsw cifl idsd'
    recipient = input("Please Enter The Email Address Where You Would Like Notifications Sent To: ")
    subject = "Your Monitored Item @ " + str(Store) + " Is Back In Stock"
    while True:
        global options
        if proxyChecker == "y":
            PROXY = [""]
            save_file = 'proxy_list.txt'
            if os.path.exists(save_file):
                with open(save_file) as f:
                    PROXY = ast.literal_eval(f.read())
            PROXY = random.choice(PROXY)
            print("Proxy Selected: " + PROXY)
            option.add_argument('--proxy-server=%s' % (PROXY))
        elif proxyChecker == "n":
            print("Monitoring without proxies.")
            linespace()
        else:
            print("Invalid Input. Please enter \'y\' or \'n\'.")
            linespace()
            continue
        userAgent = user_agent_rotator.get_random_user_agent()
        option.add_argument(f'user-agent={userAgent}')
        browser = webdriver.Chrome(executable_path=Driver_Path, options=option)
        linespace()
        browser.delete_all_cookies()
        browser.get("https://google.com")
        time.sleep(random.randint(1, 2))
        try:
            browser.get(input_url)
            price = browser.find_element_by_class_name("a-color-price")
            if price.text == msrpCheck:
                print("Restock Detected")
                linespace()
                send_email(user, pwd, recipient, subject, body)
            else:
                print("No Restock Detected. Trying Again Shortly")
                linespace()
        except:
            print("An error has occured. Your proxy was likely blocked. Retry with residential proxies or don't use proxies.")
            linespace()
        finally:
            browser.quit()
            time.sleep(random.randint(60, 80))
            linespace()


# Walmart.com Monitor
def walmartmonitor():
    print("Please Note: This is currently experimental and requires very good proxies.")
    linespace()
    body = str(input_url) + ' IS BACK IN STOCK!'
    user = 'JqMarshBooking@gmail.com'
    pwd = 'kase cdsw cifl idsd'
    recipient = input("Please Enter The Email Address Where You Would Like Notifications Sent To: ")
    subject = "Your Monitored Item @ " + str(Store) + " Is Back In Stock"
    while True:
        global options
        PROXY = [""]
        save_file = 'proxy_list.txt'
        if os.path.exists(save_file):
            with open(save_file) as f:
                PROXY = ast.literal_eval(f.read())
        PROXY = random.choice(PROXY)
        userAgent = user_agent_rotator.get_random_user_agent()
        option.add_argument('--proxy-server=%s' % (PROXY))
        option.add_argument(f'user-agent={userAgent}')
        browser = webdriver.Chrome(executable_path=Driver_Path, options=option)
        linespace()
        browser.delete_all_cookies()
        browser.get("https://google.com")
        time.sleep(random.randint(1, 2))
        try:
            browser.get(input_url)
            addtocart = browser.find_element_by_class_name('spin-button-children')
            if addtocart:
                print("Restock Detected")
                linespace()
                send_email(user, pwd, recipient, subject, body)
        except:
            print("No Restock Detected. Trying Again Shortly.")
            linespace()
        finally:
            browser.quit()
            time.sleep(random.randint(60, 80))
            linespace()


# Amazon.com Monitor
def bestbuymonitor():
    print("Please Note: This is currently experimental and requires very good proxies.")
    linespace()
    proxyChecker = input("Would you like to use proxies? (Residential Proxies Only) - If you start getting errors; restart the program without using proxies. [y/n]: ")
    linespace()
    body = str(input_url) + ' IS BACK IN STOCK!'
    user = 'JqMarshBooking@gmail.com'
    pwd = 'kase cdsw cifl idsd'
    recipient = input("Please Enter The Email Address Where You Would Like Notifications Sent To: ")
    subject = "Your Monitored Item @ " + str(Store) + " Is Back In Stock"
    while True:
        global options
        if proxyChecker == "y":
            PROXY = [""]
            save_file = 'proxy_list.txt'
            if os.path.exists(save_file):
                with open(save_file) as f:
                    PROXY = ast.literal_eval(f.read())
            PROXY = random.choice(PROXY)
            print("Proxy Selected: " + PROXY)
            option.add_argument('--proxy-server=%s' % (PROXY))
        elif proxyChecker == "n":
            print("Monitoring without proxies.")
            linespace()
        else:
            print("Invalid Input. Please enter \'y\' or \'n\'.")
            linespace()
            continue

        userAgent = user_agent_rotator.get_random_user_agent()
        option.add_argument(f'user-agent={userAgent}')
        browser = webdriver.Chrome(executable_path=Driver_Path, options=option)
        linespace()
        browser.delete_all_cookies()
        browser.get("https://google.com")
        try:
            time.sleep(random.randint(3, 5))
            browser.get(input_url)
            addtocart = browser.find_element_by_class_name("btn-leading-ficon")
            if addtocart:
                print("Restock Detected")
                linespace()
                send_email(user, pwd, recipient, subject, body)
        except:
            print("No Restock Detected. Trying Again Shortly.")
            linespace()
        finally:
            time.sleep(1)
            browser.quit()
            time.sleep(random.randint(60, 100))
            linespace()



# Amazon.com Monitor
def targetmonitor():
    print("Please Note: This is currently experimental and requires very good proxies.")
    linespace()
    body = str(input_url) + ' IS BACK IN STOCK!'
    user = 'JqMarshBooking@gmail.com'
    pwd = 'kase cdsw cifl idsd'
    recipient = input("Please Enter The Email Address Where You Would Like Notifications Sent To: ")
    subject = "Your Monitored Item @ " + str(Store) + " Is Back In Stock"
    while True:
        global options
        PROXY = [""]
        save_file = 'proxy_list.txt'
        if os.path.exists(save_file):
            with open(save_file) as f:
                PROXY = ast.literal_eval(f.read())
        PROXY = random.choice(PROXY)
        userAgent = user_agent_rotator.get_random_user_agent()
        option.add_argument('--proxy-server=%s' % (PROXY))
        option.add_argument(f'user-agent={userAgent}')
        browser = webdriver.Chrome(executable_path=Driver_Path, options=option)
        linespace()
        browser.delete_all_cookies()
        browser.get("https://google.com")
        time.sleep(random.randint(1, 2))
        try:
            browser.get(input_url)
            addtocart = browser.find_element_by_class_name('styles__StyledButton-sc-1f2lsll-0')
            if addtocart:
                print("Restock Detected")
                linespace()
                send_email(user, pwd, recipient, subject, body)
        except:
            print("No Restock Detected. Trying Again Shortly.")
            linespace()
        finally:
            time.sleep(60)
            browser.quit()
            time.sleep(random.randint(60, 120))
            linespace()



# Script Selector, starts the input script
def main():
    if Store == 'Amazon':
        amazonmonitor()
    elif Store == 'Pokemon Center Japan':
        pokemoncentermonitorjpn()
    elif Store == 'Walmart':
        walmartmonitor()
    elif Store == 'Target':
        targetmonitor()
    elif Store == 'Bestbuy':
        bestbuymonitor()
    elif Store == "Pokemon Center":
        pokemoncentermonitor()
    else:
        print("Error: ")
        print(
            "The store \'" + Store + "\' wasn\'t recognized, please input \'Amazon\', \'Walmart\', \'Target\', \'Bestbuy\', or \'Pokemon Center\' ")

# Runs the script selector
if __name__ == '__main__':
    urllib3.disable_warnings()
    main()
