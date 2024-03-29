# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class FirstprojectPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        #Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value =adapter.get(field_name)
                adapter[field_name] = value. strip()

        #Category & Product Type --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        #Price -- convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax','tax']
        for price_key in price_keys: 
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        #Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_string = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_string[0])

        #Review from string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        stars_string = adapter.get('stars')
        split_string_array = stars_string.split(' ')
        star_text_value = split_string_array[1].lower()
        if star_text_value == "zero":
            adapter['stars'] = 0
        elif star_text_value == "one":
            adapter['stars'] = 1
        elif star_text_value == "two":
            adapter['stars'] = 2
        elif star_text_value == "three":
            adapter['stars'] = 3
        elif star_text_value == "four":
            adapter['stars'] = 4
        elif star_text_value == "five":
            adapter['stars'] = 5


        return item

class SaveToMySQLPipeLine:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost', 
            user = 'root',
            password = '',
            database = 'books'
        )
        self.cur = self.conn.cursor()
        
    def process_item(self, item, spider): 
        #insert data into table
        return item
    def close_spider(self, spider): 
        self.cur.close()
        self.conn.close()
        