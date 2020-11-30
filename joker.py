import re
import requests
from bs4 import BeautifulSoup

api_token = 'ef7af10d7729afd44f0445b16ad2a25b1dd24332d9bf0c6ac01ccf13e04d5860'
dmapi_url = 'https://dmapi.joker.com/request/'
domain = input('Please enter the domain name: ')
status = ''

# Extracting live USD price from Bonbast.com
bonbast_data = requests.get('https://www.bonbast.com').text
soup = BeautifulSoup(bonbast_data, "lxml")
USD_rate = soup.find("span", attrs={"id": "usd1_top"})
USD_rate = str(USD_rate)
USD_rate = re.search('>(.*)<', USD_rate)
if USD_rate:
    USD = USD_rate.group(1)
    USD = USD.strip()
    m = re.search(",", USD)
    USD = USD[:m.start()] + USD[m.end():]
    USD = float(USD)*1.5  # Final USD rate
 

#Connects to Joker.com API
r = requests.get(dmapi_url+'login?api_key='+api_token)

#the raw output of the login info stored as normal text
output = r.text

#Extracts the session ID from the output
sid = re.search('Auth-Sid:' '(.+?)\n', output)
if sid:
    sessionID = sid.group(1)
    sessionID = sessionID.strip()
    #print (sessionID)

#check domain status (registerd or available) and check if its premium or not
def domain_status():
    send_request = dmapi_url+'domain-check?domain='+domain+'&auth-sid='+sessionID
    #print (send_request)
    report = requests.get(send_request)
    report = report.text
    report1 = re.search('domain-status:' '(.+?)\n', report)
    if report:
        status = report1.group(1)  
        print ("Domain status: ",status)
        
    
    report2 = re.search('domain-class:' '(.+?)\n', report)
    if report:
        domain_class = report2.group(1)  
        print ("Domain class: ",domain_class)


#https://dmapi.joker.com/request/domain-check?domain=yazd.shop&check-price=create&auth-sid=4175482943ad85d34df9a6b648f68eff60aba484
def check_price():
    if status == 'unavailable':

        send_request = dmapi_url+'domain-check?domain='+domain+'&check-price=renew'+'&auth-sid='+sessionID
        print (send_request)
        report = requests.get(send_request)
        report = report.text
        report = re.search('domain-price-renew:' '(.+?)\n', report)
        if report:
            price = report.group(1)  
            price = price.strip()
            price = re.search("(.*) USD",price)
            price = price.group(1)
            price = float(price)
            print ("Domain premium renew price:" ,price," USD")
            print ("Domain premium renew price:",price*USD," Toman")
    else:

        send_request = dmapi_url+'domain-check?domain='+domain+'&check-price=create'+'&auth-sid='+sessionID
        print (send_request)
        report = requests.get(send_request)
        report = report.text
        report = re.search('domain-price-create:' '(.+?)\n', report)
        if report:
            price = report.group(1)  
            price = price.strip()
            price = re.search("(.*) USD",price)
            price = price.group(1)
            price = float(price)
            print ("Domain premium create price:" ,price," USD")
            print ("Domain premium create price:",price*USD," Toman")





# check domain restore price
def restore_price():

    send_request = dmapi_url+'domain-check?domain=' + \
        domain+'&check-price=restore'+'&auth-sid='+sessionID
    #print (send_request)
    report = requests.get(send_request)
    report = report.text
    rp = re.search('domain-price-restore:(.+?)USD', report)
    if rp:
        rs_price = rp.group(1)
        rs_price = rs_price.strip()
        rs_price = float(rs_price)
        print("Restore price: ",rs_price, " USD")

    send_request = dmapi_url+'domain-check?domain=' + \
    domain+'&check-price=renew'+'&auth-sid='+sessionID
    report = requests.get(send_request)
    report = report.text

    rp = re.search('domain-price-renew:(.+?)USD', report)
    if rp:
        rn_price = rp.group(1)
        rn_price = rn_price.strip()
        rn_price = float(rn_price)
        print ("Renew price: ",rn_price, " USD")
    final_price = rs_price + rn_price
    print ("Total cost: ",final_price, " USD")


# check domain renew price
#def renew_price():
#
#    send_request = dmapi_url+'domain-check?domain=' + \
#        domain+'&check-price=renew'+'&auth-sid='+sessionID
#        print (send_request)
#    report = requests.get(send_request)
#    report = report.text
#        print (report)
#    rp = re.search('domain-price-renew:(.+?)USD', report)
#    if rp:
#        rn_price = rp.group(1)
#        rn_price = rn_price.strip()
#        rn_price = float(rn_price)
#        print(rn_price)

domain_status()
check_price()

