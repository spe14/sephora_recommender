import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
pd.options.mode.chained_assignment = None
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

service = Service(executable_path='/usr/local/bin/chromedriver')
options = Options()
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(service=service, options=options)

# def delay():
#    	time.sleep(random.randint(3, 10))
	
def lazy_loading():
    element = driver.find_element(By.TAG_NAME, 'body')
    count = 0
    while count < 10:
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        count += 1

def scroll():
    product_count = driver.find_element(By.XPATH, "//div[@class='css-unii66']/p").text
    product_count = product_count.split(' ')
    product_count = int(product_count[2])
    clicks = 0
    while clicks < 1:
        try:
            lazy_loading()
            driver.find_element(By.XPATH, "//div[@class='css-unii66']/button").click()
            time.sleep(2)
            clicks += 1
        except:
            clicks += 1
            pass
        lazy_loading

def get_product_links(products):
    for p in products.find_all('div', {'class': 'css-foh208'}):
        for p_link in p.find_all('a'):
            if p_link['href'].startswith('https:'):
                product_links.append(p_link['href'])
            else:
                product_links.append('https://www.sephora.com' + p_link['href'])

def get_links(products):
    for p in products.find_all('div', {'class': 'css-1qe8tjm'}):
        for p_link in p.find_all('a'):
            if p_link['href'].startswith('https:'):
                product_links.append(p_link['href'])
            else:
                product_links.append('https://www.sephora.con' + p_link['href'])

def extract_content(url):
    try:
        driver.get(url)
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='css-1kna575']"))).click()
        except:
            pass
        elem = driver.find_element(By.TAG_NAME, 'body')
        num = 20
        while num:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            num -= 1
        page_content = driver.page_source
        page_soup = BeautifulSoup(page_content, 'html.parser')
        return page_soup
    except:
        pass

# url = "https://www.sephora.com/shop/cheek-makeup"
# url = "https://www.sephora.com/shop/lips-makeup"
# url = "https://www.sephora.com/shop/eyebrow-makeup-pencils"
# url = "https://www.sephora.com/shop/eyeliner"
# url = "https://www.sephora.com/shop/mascara"
# url = "https://www.sephora.com/shop/eyeshadow"
# url = "https://www.sephora.com/shop/foundation-makeup"
# url = "https://www.sephora.com/shop/concealer"
# url = "https://www.sephora.com/shop/makeup-primer-face-primer"
# url = "https://www.sephora.com/shop/setting-powder-face-powder"
url = "https://www.sephora.com/shop/luminizer-luminous-makeup"



driver.get(url)

# Continuously clicking the button to show more products till everything is loaded
scroll()

# Converting the content of the page to BeautifulSoup object
content = driver.page_source
homepage_soup = BeautifulSoup(content, 'html.parser')

# Fetching the product links of all items
product_links = []
# print(len(product_links))
products = homepage_soup.find_all('div', attrs={"class": "css-1322gsb"})[0]
# get_product_links(products)               # Fetching the product links that does not have lazy loading
get_links(products)  # Fetching the product links that have lazy loading

# print(len(product_links))
# print(product_links)

# info to get for each product
# category (eye, face, lips, etc)
def category_data(soup):
    # category = driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(3) > main > div:nth-child(1) > nav > ol > li:nth-child(3) > a').text
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, 'a.css-sdfa4l.eanm77i0')
        data['category'].iloc[product] = elements[-1].text
    except:
        data['category'].iloc[product] = "Category unavailable"

# brand
def brand_data(soup):
    try:
        brand = soup.find('a', attrs={"data-at": "brand_name"}).text
        data['brand'].iloc[product] = brand
    except:
        brand = 'Brand name not available'
        data['brand'].iloc[product] = brand

# product name
def product_name(soup):
    try:
        name = soup.find('span', attrs={"data-at":"product_name"}).text
        data['product_name'].iloc[product] = name
    except:
        name = 'Product name not available'
        data['product_name'].iloc[product] = name

# reviews - sentiment analysis
def review_data(soup):
    try:
        if driver.find_element(By.XPATH, '//h2[@class="css-1bu59gz eanm77i0"]').text != "Ratings & Reviews (0)":
            try:
                reviews_list = []
                reviews = driver.find_elements(By.XPATH, "//div[@class='css-c95msn eanm77i0']")
                # time.sleep(5)
                for r in reviews:
                    reviews_list.append(r.text)
                data['reviews'].iloc[product] = reviews_list
            except:
                data['reviews'].iloc[product] = "No reviews available"
        else:
            data['reviews'].iloc[product] = "No reviews available"
    except:
        data['reviews'].iloc[product] = "No reviews available"

# love count
def like_count(soup):
    try:
        like = soup.find('span', attrs={'class':'css-jk94q9'}).text
        data['like_count'].iloc[product] = like
    except:
        like = "Like count not available"
        data['like_count'].iloc[product] = like

# rating
def rating_data(soup):
    try:
        rating = soup.find('span', attrs={'class': 'css-1tbjoxk'})['aria-label']
        data['rating'].iloc[product] = rating
    except:
        rating = 'Rating not available'
        data['rating'].iloc[product] = rating


# price
def price_data(soup):
    try:
        price = soup.find('b', attrs={'class': 'css-0'}).text
        data['price'].iloc[product] = price
    except:
        price = 'Price not available'
        data['price'].iloc[product] = price


# ingredients
def ingredient_data(soup):
    try:
        for ingredient in soup.find('div', attrs={'class':'css-1ue8dmw eanm77i0'}):
            if len(ingredient.contents) == 1:
                try:
                    data['ingredients'].iloc[product] = ingredient.contents[0].text
                except:
                    data['ingredients'].iloc[product] = ingredient.contents[0]
            else:
                data['ingredients'].iloc[product] = ingredient.contents[1]
    except:
        data['ingredients'].iloc[product] = 'Ingredients data not available'
 

def find_element_by_xpath():
    try:
        section = driver.find_element(By.XPATH, "//div[@class='css-32uy52 eanm77i0']").text
        split_sections = section.split('\n')
        return split_sections
    except:
        pass
        

# product description - sentiment analysis
def product_description():
    split_section = find_element_by_xpath()
    try:
        for s in split_section:
            key_and_value = s.split(':')
            try:
                if key_and_value[0] == 'What it is':
                    data['description'].iloc[product] = key_and_value[1]
            except:
                data['description'].iloc[product] = "Description unavailable"
    except:
        pass

def qualities(soup):
    try:
        qual_list = []
        quals = soup.find_all('button', attrs={'class': 'css-13amwq4 eanm77i0'})
        for q in quals:
            qual_list.append(q.text)
        data['qualities'].iloc[product] = qual_list
    except:
        data['qualities'].iloc[product] = "No qualities listed"

def review_count(soup):
    try:
        rev_count = soup.find('span', attrs={'data-at': 'number_of_reviews'}).text
        data['number_of_reviews'].iloc[product] = rev_count
    except:
        data['number_of_reviews'].iloc[product] = "Review count not available"

data_dict = {'product_url': [], 'brand': [], 'category': [], 'product_name': [], 'number_of_reviews': [], 
             'like_count': [], 'rating': [], 'price': [], 'description': [], 'qualities': [], 'ingredients': [], 'reviews': []}

data = pd.DataFrame(data_dict)
data['product_url'] = product_links

for product in range(len(data)):
    product_url = data['product_url'].iloc[product]
    product_content = extract_content(product_url)

    brand_data(product_content)
    category_data(product_content)
    product_name(product_content)
    review_count(product_content)
    like_count(product_content)
    rating_data(product_content)
    price_data(product_content)
    product_description()
    ingredient_data(product_content)
    review_data(product_content)
    qualities(product_content)

driver.quit()
data.to_csv('highlighter_products.csv')