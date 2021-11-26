from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

CHROME_DRIVER_PATH = "D:\\Downloads\\100DaysOfCode\\Development\\chromedriver_win32\\chromedriver.exe"
FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSfqIA2az5-RFa66UsJVaxCaNAnb5vEAkySvuCNxtAjeh9s6wA/viewform?usp=sf_link'
ZILLOW_LINK = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.64283262612446%2C%22east%22%3A-122.19719969155415%2C%22south%22%3A37.665492929258825%2C%22north%22%3A37.90280338294463%7D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9,sr-GB;q=0.8,sr;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

time.sleep(0.5)


# Page source code saved in a file for testing so I don't spam the hell out of their servers
# with open(file="html_file\\zillow.html") as file:
#     data = file.read()


response = requests.get(url=ZILLOW_LINK, headers=HEADERS).text
soup = BeautifulSoup(markup=response, parser="html.parser", features="lxml")
price = soup.find_all(class_="list-card-price")
address = soup.find_all(class_="list-card-addr")
link = soup.find_all(name="a", class_="list-card-link list-card-link-top-margin")

prices_list = []
address_list = []
links_list = []

for member in price:
    prices_list.append(member.text)
for member in address:
    address_list.append(member.text)
for member in link:
    member_text = member.get("href")
    if "https" not in member_text:
        member_text = "https://www.zillow.com/" + member_text
    links_list.append(member_text)


driver.get(FORM_LINK)
time.sleep(1)

# Range limited to 6, can be changed to len(prices_list), left like this to only test a few results
for i in range(6):
    input_1 = driver.find_element(By.XPATH,
                                  '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_2 = driver.find_element(By.XPATH,
                                  '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_3 = driver.find_element(By.XPATH,
                                  '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    confirm_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    input_1.send_keys(f"{prices_list[i]}")
    input_2.send_keys(f"{address_list[i]}")
    input_3.send_keys(f"{links_list[i]}")
    confirm_button.click()
    send_again_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    time.sleep(1)
    send_again_button.click()
    time.sleep(1)

driver.quit()
