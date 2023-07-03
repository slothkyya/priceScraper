# Import necessary libraries
import requests  # Used for HTTP requests
import csv  # Used for CSV file operations
from bs4 import BeautifulSoup  # Used for parsing HTML
from pony import orm  # Used for object-relational mapping (ORM)
from datetime import datetime  # Used for handling date and time
import time  # Used for time-related tasks (like waiting)

# Set up the ORM database
db = orm.Database()  # Create an ORM database object
# Bind the ORM database object to a SQLite database file named 'products.db'
db.bind(provider = 'sqlite', filename = 'products.db', create_db = True)

# Define a class representing a Product entity in the ORM model
class Product(db.Entity):
    name = orm.Required(str)  # The product's name
    price = orm.Required(float)  # The product's price
    create_date = orm.Required(datetime)  # The date when the product information was stored

# Generate tables in the SQLite database according to the ORM model
db.generate_mapping(create_tables = True)

# Function for scraping Amazon product data
def amazon(session, headers, url):
    # Initialize variables
    name = None
    price = None
        
    # Try scraping the webpage up to 20 times
    for i in range(20):
        # Send a GET request to the URL
        resp = session.get(url, headers=headers)
        # Parse the HTML content of the response
        soup = BeautifulSoup(resp.text, "html.parser")
        # Try finding the product name and price if not found yet
        if name == None:
            name = search_name(soup)
        if price == None:
            price = search_price(soup)
       
        # If both name and price are found, return them
        if name and price:
            return (name, price)
        # Otherwise, wait 0.1 second before the next try
        time.sleep(0.1)
    # Return name and price (possibly None)
    return (name, price)   

# Function for finding the product name in the parsed HTML content
def search_name(soup):
    name = soup.find("span", class_="a-size-large product-title-word-break")
    if name:
        name = name.text
    return name

# Function for finding the product price in the parsed HTML content
def search_price(soup):
    price_element = soup.select_one("div.a-box-group span.a-offscreen")
    if price_element:
        try:
            # Remove the dollar sign and convert to float
            price = float(price_element.text.replace("$", ""))
            return price
        except ValueError:
            pass 
    return None

# Function for exporting the data in the ORM database to a CSV file
def export_data_to_csv():
    # Query the ORM database for all Product entities sorted by create_date
    data = Product.select().order_by(Product.create_date)
    with open("products.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Name", "Price", "Created Date"])
        # Write a row for each Product entity
        for product in data:
            name = product.name.strip()  # Remove leading and trailing spaces from name
            price = str(product.price)  # Convert price to string
            create_date = product.create_date.strftime("%Y-%m-%d %H:%M:%S")  # Format create_date as string
            writer.writerow([name, price, create])
            
def read_price_from_csv(name):
    price = None  # Default value if no matching name is found
    with open("products.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0]:
                if row[0].strip() == name.strip():
                    price = float(row[1])
                    break  # Exit the loop after finding the matching name
    return price
           
def main() :
    session = requests.Session()
    headers = {
        'User-Agent': 'computer user-agent'
    }
    urlFile = "urlRequest"
    with open(urlFile, mode="r") as file:
        for line in file:
            url = line.strip()
            data = [
                
                (amazon(session, headers, url)),
            ]   
            
            print("current item:", data)
            # loop through the data to save to the sqlite db
            with orm.db_session:
                latest_price = read_price_from_csv(data[0][0])
                if latest_price == data[0][1]:
                    print("No price update")
                else:
                    Product(name=data[0][0], price=data[0][1], create_date=datetime.now())
                    export_data_to_csv()
    
        
    
if __name__ == '__main__':
    main()
