# Flipkart Mobile Data Scraper

A Python-based web scraper that extracts mobile phone information from Flipkart's search results, including product names, prices, ratings, processor details, battery information, and camera specifications.

## Features

- **Interactive Product Search**: Prompts user to input the product category they want to search for
- **Multi-page Scraping**: Automatically scrapes data from multiple pages (up to 44 pages)
- **Comprehensive Data Extraction**: Collects product name, price, rating, processor, battery, and camera information
- **Error Handling**: Implements retry logic with random delays to handle network issues
- **Data Export**: Saves collected data to a pandas DataFrame (with optional CSV export)
- **Rate Limiting**: Includes random sleep intervals to avoid being blocked

## Prerequisites

Before running this scraper, make sure you have the following Python packages installed:

```bash
pip install pandas requests beautifulsoup4 lxml
```

## Required Dependencies

- `pandas`: For data manipulation and DataFrame creation
- `requests`: For making HTTP requests to Flipkart
- `beautifulsoup4`: For parsing HTML content
- `lxml`: HTML parser for BeautifulSoup
- `time`: For implementing delays (built-in)
- `random`: For random delay intervals (built-in)

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python flipkart_scraper.py
   ```

## Usage

1. **Run the Script**: Execute the Python file
2. **Enter Product Category**: When prompted, enter the product category you want to search for (e.g., "mobile", "smartphone", "iphone")
3. **Wait for Completion**: The script will automatically scrape data from multiple pages
4. **View Results**: The collected data will be displayed as a pandas DataFrame

## Code Implementation

### 1. Import Libraries

```python
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import random
```

These imports bring in the essential libraries needed for web scraping. `pandas` handles data manipulation, `requests` makes HTTP calls to websites, `BeautifulSoup` parses HTML content, and `time`/`random` manage delays to avoid getting blocked.

### 2. Initialize Data Storage Lists

```python
#taking empty list to store the data
product_name = []
product_price = []
product_battery = []
product_camera = []
product_processor = []
product_rating = []
```

Six empty lists are created to store different product attributes. These lists will grow as we scrape data from multiple pages, ensuring all product information is organized by category.

### 3. URL Construction Function

```python
def page(page_number)
    url ="https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+ str(page_number)
    print(url)
    print(f"Fetching data from page: {page_number}")
```

This function builds the search URL for Flipkart by taking user input for the product category and appending the page number. It prints the URL for debugging purposes.

### 4. Main Scraping Function

```python
def all(page):
    response = requests.get(page.url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page.page_number}")
        return False

    soup = BeautifulSoup(response.text, 'lxml')
    box = soup.find("div", class_="DOjaWF gdgoEp")
```

This function handles the core scraping logic. It makes an HTTP request to the page, checks if it's successful, then uses BeautifulSoup to parse the HTML and locate the main product container.

### 5. Extract Product Names

```python
    names = box.find_all("div", class_="KzDlHZ")
    for a in names:
        product_name.append(a.text)
```

Finds all product name elements using their CSS class and extracts the text content, adding each product name to the `product_name` list.

### 6. Extract Product Prices

```python
    price = box.find_all("div", class_="Nx9bqj _4b5DiR")
    for b in price:
        product_price.append(b.text)
    while len(product_price) < len(product_name):
        product_price.append("0")
```

Extracts product prices and ensures the price list has the same length as the name list by padding with "0" values for products without prices.

### 7. Extract Product Ratings

```python
    rating = box.find_all("div", class_="XQDdHH")
    for d in rating:
        product_rating.append(d.text)
    
    while len(product_rating) < len(product_name):
        product_rating.append("0")
```

Similar to prices, this extracts customer ratings and maintains data consistency by padding shorter lists with "0" values.

### 8. Extract Detailed Specifications

```python
def mobile(all):
    descriptions = all.box.find_all("ul", class_="G4BRas")
    for c in descriptions:
        all_lines = [li.text.strip() for li in c.find_all("li")]
        description_lines = all_lines[0:5]

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
```

This function extracts detailed product specifications by searching through product description lists. It uses flag variables to ensure only one specification of each type is captured per product.

### 9. Main Execution Loop

```python
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
```

The main loop iterates through 44 pages, implementing retry logic for failed requests. It includes random delays between attempts to avoid being blocked by anti-bot measures.

### 10. Data Export

```python
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
```

Finally, all collected data is organized into a pandas DataFrame for easy analysis and manipulation. The commented line allows for CSV export if needed.

## Data Processing and Phone Search System

After scraping the data, you can use the following Jupyter notebook code to clean and search through the mobile phone data:

### 1. Data Cleaning and Handling Missing Values

```python
import pandas as pd
import numpy as np
df = pd.read_csv("Flipkart_Mobile_Data.csv")
df.replace(["0",0],np.nan,inplace=True)
df.dropna(subset=["Camera"],inplace=True)
df.dropna(subset=["Price"],inplace=True)
df.dropna(subset=["Rating"],inplace=True)
print(df.isnull().sum())

df.to_csv("Flipkart_Mobile_Data.csv", index_label="Product_Number",index=False)
```

This section loads the scraped data and cleans it by replacing "0" values with NaN, then removes rows with missing Camera, Price, or Rating data. It shows how many null values remain in each column.

### 2. Extract Company Name, Storage, and Color Information

```python
df["Compny Name"]=df["Name"].str.split().str[0]
df["Storage"]=df["Name"].str.extract(r',([^)]+)\)',expand=True)
df["Colour"] = df["Name"].str.extract(r'^(?:.*?)(?:\(|,\s*)([^,]+?)(?:,|\))', expand=False)
df.to_csv("Flipkart_Mobile_Data.csv", index_label="Product_Number",index=False)
df["Name"] = df["Name"].str.replace(r'\([^)]*\)', '', regex=True)
df["Name"] = df["Name"].str.replace(r',\s*\d+\s*GB', '', regex=True)
df["Name"] = df["Name"].str.strip()
print(df["Name"])
df.to_csv("Flipkart_Mobile_Data.csv", index_label="Product_Number",index=False)
```

This code extracts useful information from product names using regex patterns:
- Company name (first word of the product name)
- Storage capacity from parentheses
- Color information from the product name
- Cleans the product name by removing storage and color details

### 3. Filter Out Budget Phones

```python
small = df[df['Price'] < 7000].index
df.drop(small, inplace=True)
df.head()
df.to_csv("Flipkart_Mobile_Data.csv", index_label="Product_Number",index=False)
```

Removes all phones priced below ₹7000 to focus on mid-range and premium devices, improving the quality of recommendations.

### 4. Remove Duplicate Entries

```python
df = df.drop_duplicates(subset=['Name','Price','Storage'], keep='first')
df.head()
df.to_csv("Flipkart_Mobile_Data.csv", index_label="Product_Number")
```

Eliminates duplicate entries based on name, price, and storage to ensure each unique phone appears only once in the dataset.

### 5. Interactive Phone Search System

```python
question=input("Hello!! do you wnat Iphone or Android")

df["price"]=df["Price"].astype(str).astype(int)
if question == "Iphone":
    apple=df.loc[df["Compny Name"]== "Apple"]
    print(apple)
    price=int(input("Your budget for this phone"))
    harsh=apple["Price"] <= price
    filtered_name=apple[harsh][["Name","Price"]]
    if filtered_name.empty:
        print("Do not have any mobile in this Range")
    else:
        print(filtered_name)
elif question == "Android":
    print(df.loc[df["Compny Name"]!= "Apple"])
    if filtered_name.empty:
        print("Do not have any Apple mobile in this Range")
```

This interactive system allows users to:
- Choose between iPhone or Android devices
- For iPhones: Enter budget and get filtered results within that price range
- For Android: Display all non-Apple devices
- Handle cases where no phones match the criteria

The search system provides a user-friendly way to find phones based on brand preference and budget constraints, making the scraped data practically useful for phone shopping decisions.

## Code Structure

### Main Components

- **Data Storage Lists**: Six lists to store different product attributes
- **`page()` Function**: Constructs the search URL based on user input and page number
- **`all()` Function**: Handles the main scraping logic for product names, prices, and ratings
- **`mobile()` Function**: Extracts detailed specifications (processor, battery, camera)
- **Main Loop**: Iterates through pages 1-44 with retry logic

### Data Fields Extracted

- **Name**: Product name/title
- **Price**: Product price in INR
- **Rating**: Customer rating
- **Processor**: Processor specifications
- **Battery**: Battery capacity and details
- **Camera**: Camera specifications

## Error Handling

The scraper includes several error handling mechanisms:

- **HTTP Status Check**: Verifies successful page retrieval (status code 200)
- **Retry Logic**: Attempts to fetch each page up to 5 times
- **Random Delays**: Implements 3-6 second delays between retries
- **Data Consistency**: Ensures all lists have equal length by padding with "0" values

## Rate Limiting

To avoid being blocked by Flipkart's anti-bot measures:
- Random delays between 1-5 seconds after each successful page
- Random delays between 3-6 seconds for retry attempts
- Processes pages sequentially rather than in parallel

## Output

The script generates a pandas DataFrame with the following columns:
- Name
- Price
- Battery
- Processor
- Camera
- Rating

### CSV Export (Optional)

Uncomment the last line to save data to CSV:
```python
df.to_csv("Flipkart_Mobile_Data.csv", index_label="Product_Number")
```

## Important Notes

### Legal and Ethical Considerations

- **Terms of Service**: Ensure your usage complies with Flipkart's Terms of Service
- **Rate Limiting**: The script includes delays to be respectful of the website's resources
- **Personal Use**: This scraper is intended for educational and personal use only

### Limitations

- **Dynamic Content**: May not work if Flipkart changes their HTML structure
- **Anti-bot Measures**: Flipkart may implement additional anti-scraping measures
- **Data Accuracy**: Some products may have missing specifications (handled as "0")

### Known Issues

- **URL Construction**: There's a typo in the URL construction (`{category}e` instead of `{category}`)
- **Function Structure**: The current structure has some logical issues that may need refactoring
- **Error Handling**: Some edge cases may not be properly handled

## Troubleshooting

### Common Issues

1. **"Failed to retrieve page"**: Check your internet connection and verify the URL is accessible
2. **Empty DataFrame**: Ensure Flipkart's HTML structure hasn't changed
3. **Missing Data**: Some products may not have all specifications available

### Debug Mode

The script prints various debug information:
- Page URLs being accessed
- Current page number being processed
- Length of each data list
- Success/failure status for each page

## Future Improvements

- Add support for different product categories beyond mobiles
- Implement database storage options
- Add data validation and cleaning
- Create a GUI interface
- Add configuration file for customizable settings
- Implement better error logging

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is for educational purposes only. Please respect Flipkart's Terms of Service and robots.txt file.

## Disclaimer

This scraper is provided as-is for educational purposes. Users are responsible for ensuring their usage complies with applicable laws and website terms of service. The authors are not responsible for any misuse of this tool.
