# priceScraper
a Python script for scraping product names and prices from Amazon, storing the data in an SQLite database, and exporting the data to a CSV file.
Prerequisites


## Dependencies

- requests
- BeautifulSoup4
- Pony ORM
- csv
- datetime
- time

## Setup and Usage

1. Install the required Python packages if you haven't already.

    ```bash
    pip install -r requirements.txt
    ```

2. Prepare a file named `urlRequest` containing the URLs of the Amazon products you want to scrape. Each URL should be on a new line.

3. change the "User-Agent" in main(), line 98

4.  Run the script using Python.


The script will automatically scrape the data, store it in a SQLite database, and update a CSV file if there are changes in the product price. The SQLite database and the CSV file are both named `products`.

## Project Structure

- `main.py`: This is the main Python script that contains all the scraping logic.
- `products.db`: This is the SQLite database where the product data is stored.
- `products.csv`: This is the CSV file where the product data is exported if there are changes in the product price.

## Functions

- `amazon(session, headers, url)`: This function scrapes the product name and price from the specified Amazon URL.
- `search_name(soup)`: This function extracts the product name from the BeautifulSoup object.
- `search_price(soup)`: This function extracts the product price from the BeautifulSoup object.
- `export_data_to_csv()`: This function exports the product data from the SQLite database to a CSV file.
- `read_price_from_csv(name)`: This function reads the product price from the CSV file based on the product name.


