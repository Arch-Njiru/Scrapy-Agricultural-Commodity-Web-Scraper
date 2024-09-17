import scrapy
import os
import csv

class CommoditySpider(scrapy.Spider):
    name = "commodities"

    # Allow users to pass arguments like base URL, product numbers, column names, and CSV file name
    def __init__(self, base_url=None, product_ids=None, column_names=None, csv_file_name="commodity_data.csv", *args, **kwargs):
        super(CommoditySpider, self).__init__(*args, **kwargs)
        
        # Set default base URL if not provided
        self.base_url = base_url or 'https://amis.co.ke/site/market'
        
        # Convert the product_ids string to a list of integers
        if product_ids:
            self.product_ids = [int(p.strip()) for p in product_ids.split(',')]
        else:
            self.product_ids = [1]  # Default product to scrape if no product IDs are given

        # Set default CSV file name
        self.csv_file_name = csv_file_name

        # Convert the column names string to a list if provided, or use default column names
        if column_names:
            self.column_names = column_names.split(',')
        else:
            self.column_names = ['commodity', 'classification', 'grade', 'market', 'wholesale', 'retail', 'supply_volume', 'county', 'date']

        # Ensure CSV file is created with headers
        if not os.path.exists(self.csv_file_name):
            with open(self.csv_file_name, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.column_names)

    def start_requests(self):
        """Initiate the scraping requests for the selected products."""
        for product_id in self.product_ids:
            url = f'{self.base_url}?product={product_id}&per_page=3000'
            yield scrapy.Request(url=url, callback=self.parse, meta={'product_id': product_id, 'page_number': 1})

    def parse(self, response):
        """Parse the table rows and handle pagination."""
        product_id = response.meta['product_id']
        page_number = response.meta['page_number']

        # Write scraped data to CSV
        for row in response.css('tr'):
            data = {
                'commodity': row.css('td:nth-child(1)::text').get(),
                'classification': row.css('td:nth-child(2)::text').get(),
                'grade': row.css('td:nth-child(3)::text').get(),
                'market': row.css('td:nth-child(5)::text').get(),
                'wholesale': self.extract_price(row.css('td:nth-child(6)::text').get()),
                'retail': self.extract_price(row.css('td:nth-child(7)::text').get()),
                'supply_volume': row.css('td:nth-child(8)::text').get(default='N/A'),
                'county': row.css('td:nth-child(9)::text').get(),
                'date': row.css('td:nth-child(10)::text').get(),
            }

            if data['commodity']:  # Skip any empty rows
                with open(self.csv_file_name, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([data.get(col.strip()) for col in self.column_names])

        # Handle pagination
        next_page_url = f"{self.base_url}/{3000 * page_number}?product={product_id}&per_page=3000"
        if len(response.css('tr')) > 1:  # Check if there are more rows (pagination needed)
            yield scrapy.Request(next_page_url, callback=self.parse, meta={'product_id': product_id, 'page_number': page_number + 1})

    def extract_price(self, price_str):
        """Extract price and handle missing or empty values."""
        if price_str and price_str.strip() != '-' and price_str.strip():
            return price_str.split('/')[0].strip()
        else:
            return 'N/A'
