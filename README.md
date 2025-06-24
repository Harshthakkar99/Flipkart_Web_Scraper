# 📱 Flipkart Mobile Scraper - Python Script with Comments

```python
# 📦 Import Required Libraries
import pandas as pd                  # For creating DataFrame and data storage
import requests                      # For sending HTTP requests
import time                          # For delay to avoid IP blocking
from bs4 import BeautifulSoup        # For parsing HTML content
import random                        # For adding random sleep intervals

# 🗃️ Initialize empty lists to store scraped data
product_name = []
product_price = []
product_battery = []
product_camera = []
product_processor = []
product_rating = []

# 🔗 Generate Flipkart search page URL and take input for product
def page(page_number):
    category = input("Which product do you want to purchase? ")
    
    # 🛒 Construct the URL with the given category and page number
    url = f"https://www.flipkart.com/search?q={category}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page_number}"
    print(url)
    print(f"Fetching data from page: {page_number}")

    # Send request to the page
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Failed to retrieve page {page_number}")
        return False

    # 🌐 Parse the page content
    soup = BeautifulSoup(response.text, 'lxml')

    # 🎯 Find the main product container
    box = soup.find("div", class_="DOjaWF gdgoEp")
    if not box:
        print("⚠️ Product box not found")
        return False

    # 📝 Extract Product Names
    names = box.find_all("div", class_="KzDlHZ")
    for a in names:
        product_name.append(a.text)

    # 💰 Extract Prices
    price = box.find_all("div", class_="Nx9bqj _4b5DiR")
    for b in price:
        product_price.append(b.text)

    # Ensure length consistency
    while len(product_price) < len(product_name):
        product_price.append("0")

    # ⭐ Extract Ratings
    rating = box.find_all("div", class_="XQDdHH")
    for d in rating:
        product_rating.append(d.text)

    # Ensure rating count matches
    while len(product_rating) < len(product_name):
        product_rating.append("0")

    # 🛠️ Extract Specs - Call secondary function
    mobile(box)

    return True

# 🔍 Extract Battery, Processor, Camera
def mobile(box):
    descriptions = box.find_all("ul", class_="G4BRas")

    for c in descriptions:
        all_lines = [li.text.strip() for li in c.find_all("li")]
        description_lines = all_lines[0:5]  # Limit to top 5 specs

        # Flags to track if specific specs found
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

        # Fill missing data with "0"
        if not processor_found:
            product_processor.append("0")
        if not battery_found:
            product_battery.append("0")
        if not camera_found:
            product_camera.append("0")

# 🔁 Loop through multiple Flipkart pages
for i in range(1, 45):  # Pages 1 to 44
    print(f"\n🌐 Scraping Page {i}")
    success = False

    # Retry mechanism - 5 attempts max
    for attempt in range(5):
        success = page(i)
        if success:
            break
        else:
            print(f"🔁 Retrying page {i}, attempt {attempt + 1}")
            time.sleep(random.randrange(3, 6))  # Sleep between retries

    if not success:
        print(f"⚠️ Skipping page {i} after 5 failed attempts.")
    else:
        print(f"✅ Page {i} scraped successfully.")
        time.sleep(random.randrange(1, 5))  # Random delay between pages

# 📊 Create DataFrame from collected data
df = pd.DataFrame({
    "Name": product_name,
    "Price": product_price,
    "Battery": product_battery,
    "Processor": product_processor,
    "Camera": product_camera,
    "Rating": product_rating
})

# 🖨️ Show sample scraped data
print(df)

# 💾 Export data to CSV (uncomment to use)
# df.to_csv("Flipkart_Mobile_Data.csv", index_label="Product_Number")