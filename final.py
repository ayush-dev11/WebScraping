from cgitb import text
import json
from cmath import asin
import csv
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
import json



PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
file = open('AmazonScraping.csv')

#MongoDB connection
client = MongoClient("mongodb+srv://ayushSharma:siuuuRony@mycluster.o5frq.mongodb.net/scraping?retryWrites=true&w=majority")
db = client.scraping




type(file)
csvreader = csv.reader(file)
header = []
list2 = []
rows = []
header = next(csvreader)

for row in csvreader:
    rows.append(row)


#scraping for 0th to 50 entry from the csv file - this can be customized according to the requirement by changing values in the for loop

for i in range(0,50):
    print(i)
    scraped_data = {}

    driver.get("https://www.amazon.{country}/dp/{asin}".format(country = rows[i][3],asin = rows[i][2]))
    
    list1 = driver.title.split()
    print(list1)
    if(("Books" in list1) or ("Livres" in list1) or ("Libri" in list1) or ("Libros" in list1)):
        print("Hello")
        try:
            product_title = WebDriverWait(driver,20).until(  
                EC.presence_of_element_located((By.ID,"productTitle"))
            )
            print(product_title.text)

            product = driver.find_element(By.ID, "a-autoid-3")
            product_price = product.find_element(By.CLASS_NAME, "a-color-base")
            


            print(product_price.text)
            details = driver.find_element(By.ID, "detailBulletsWrapper_feature_div")
            details_precise = details.find_element(By.TAG_NAME, "ul")
            print(details_precise.text)

            image_container = driver.find_element(By.ID, "img-canvas")
            img_tag = driver.find_element(By.TAG_NAME, "img")
            img_url = img_tag.get_attribute("src")
            print(img_url)

            scraped_data["title"] = product_title.text
            scraped_data["price"] = product_price.text
            scraped_data["details"] = details_precise.text
            scraped_data["image_url"] = img_url
            list2.append(scraped_data)
            

        except:
            driver.quit()

print(list2)

scraped_json_data = json.dumps(list2)
with open('file2.json', 'w') as f:
    json.dump(scraped_json_data, f)

## uploading data to mongodb server
for element in list2:
    result = db.scraped.insert_one(element).inserted_id


driver.quit()











        





       
