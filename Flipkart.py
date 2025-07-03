import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import random
#taking empty list to store the data
product_name = []
product_price = []
product_battery = []
product_camera = []
product_processor = []
product_rating = []

#giving link to scrap the data
def page(page_number):
    url ="https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+ str(page_number)
    print(url)
    print(f"Fetching data from page: {page_number}")

#checking if given link is valid or working or not
def all(page):
    response = requests.get(page.url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page.page_number}")
        return False

    soup = BeautifulSoup(response.text, 'lxml')
#making box so data will be taken from specific box
    box = soup.find("div", class_="DOjaWF gdgoEp")

#extrect the mobile name from website
    names = box.find_all("div", class_="KzDlHZ")
    for a in names:
        product_name.append(a.text)
    
#extrect the price of mobile from website
    price = box.find_all("div", class_="Nx9bqj _4b5DiR")
    for b in price:
        product_price.append(b.text)
    while len(product_price) < len(product_name):
        product_price.append("0")
#extrect the rating of mobile from website
    rating = box.find_all("div", class_="XQDdHH")
    for d in rating:
        product_rating.append(d.text)
    
    while len(product_rating) < len(product_name):
        product_rating.append("0")
    
#extrect the processor,battery,camera from website
def mobile(all):
    descriptions = all.box.find_all("ul", class_="G4BRas")
    for c in descriptions:
        all_lines = [li.text.strip() for li in c.find_all("li")]
        description_lines = all_lines[0:5]

        #using flag maethod so only single data is extracted from lists
        processor_found = False
        battery_found = False
        camera_found = False

        for z in description_lines:
            if "Processor" in z and not processor_found:
                product_processor.append(z)
                processor_found = True
            if "Battery" in z and not battery_found:
                product_battery.append(z)
                battery_found = True
            if "Camera" in z and not camera_found:
                product_camera.append(z)
                camera_found = True

        # if value is not found the it will append 0
        if not processor_found:
            product_processor.append("0")
        if not battery_found:
            product_battery.append("0")
        if not camera_found:
            product_camera.append("0")
    
    print("Name", len(product_name))
    print("price", len(product_price))
    print("rating", len(product_rating))
    print("processor", len(product_processor))
    print("battery", len(product_battery))
    print("camera", len(product_camera))       
    return True

for i in range(1,45):
    print(i)
    success = False
    for attempt in range(5):
        success = page(i)
        if success:
            break
        else:
            print(f"Retrying page {i}, attempt {attempt + 1}")
            time.sleep(random.randrange(3, 6))

    if not success:
        print(f"Skipping page {i} after 5 failed attempts.")
    else:
        print(f"Page number {i} done")
        time.sleep(random.randrange(1, 5))

df = pd.DataFrame({
    "Name": product_name,
    "Price": product_price,
    "Battery": product_battery,
    "Processor": product_processor,
    "Camera": product_camera,
    "Rating": product_rating
})
print(df)
#df.to_csv("Flipkart_Mobile_Data.csv", index_label="Product_Number")

