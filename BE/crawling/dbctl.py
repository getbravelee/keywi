import mysql.connector
from getpass4 import getpass
from base import StoreData

Data=StoreData()
'''
CREATE TABLE category (
    category_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    parent_id INT NULL
);

CREATE TABLE products (
    product_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    product_url VARCHAR(500) NOT NULL,
    product_image VARCHAR(255),
    options VARCHAR(500),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE products_descriptions (
    product_description_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    description text NOT NULL,
    description_order INT NOT NULL,
    content_type ENUM('text', 'image', 'hr', 'embed', 'gif') NOT NULL,
    hyperlink VARCHAR(500),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
'''

create_products_table_query = f"""
CREATE TABLE products (
    product_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    product_url VARCHAR(500) NOT NULL,
    product_image VARCHAR(255),
    options VARCHAR(500),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
)
"""

create_products_descriptions_table_query = f"""
CREATE TABLE products_descriptions (
    product_description_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    description text NOT NULL,
    description_order INT NOT NULL,
    content_type ENUM('text', 'image', 'hr', 'embed', 'gif', 'link') NOT NULL,
    hyperlink VARCHAR(500),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
"""

class DBs:
    def __init__(self):
        self.DB = mysql.connector.connect(
            host="localhost", #input("host: "),
            user="wsl_user", #input("mysql user: "),
            password="Tkvl123!", #getpass("mysql password: "),
            database="KeyWi"
        )
        self.cursor = self.DB.cursor()
    
    def __str__(self):
        return self.DB.is_connected()
        
    def insert_category(self, category_name, parent_id=None):
        self.cursor.execute("INSERT INTO category (category_name, parent_id) VALUES (%s, %s)", (category_name, parent_id))
        self.DB.commit()
        return self.cursor.lastrowid

    def insert_product(self, category_id, product_name, price, product_url, product_image=None, options=None):
        self.cursor.execute(
            "INSERT INTO products (category_id, product_name, price, product_url, product_image, options) VALUES (%s, %s, %s, %s, %s, %s)",
            (category_id, product_name, price, product_url, product_image, options)
        )
        self.DB.commit()
        return self.cursor.lastrowid

    def insert_product_description(self, product_id, detail_description, description_order, content_type, hyperlink=None):
        self.cursor.execute(
            "INSERT INTO products_descriptions (product_id, description, description_order, content_type, hyperlink) VALUES (%s, %s, %s, %s, %s)",
            (product_id, detail_description, description_order, content_type, hyperlink)
        )
        self.DB.commit()
        
    def exist_link(self, product_id):
        self.cursor.execute("""
            SELECT COUNT(*) FROM products_descriptions
            WHERE product_id = %s AND content_type = 'link' AND hyperlink IS NULL
        """, (product_id,))
        result = self.cursor.fetchone()
        return result[0]

    def update_link(self, strd, url, des_id):
        self.cursor.execute("UPDATE products_descriptions SET description = %s, hyperlink = %s WHERE product_description_id = %s", 
                            (strd, url, des_id))
        result = self.DB.commit()
        print(result)

    def get_product_id_by_name(self, product_name):
        self.cursor.execute( "SELECT product_id FROM products WHERE product_name = %s",  (product_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_link_description_ids(self, product_id):
        self.cursor.execute("""
            SELECT product_description_id 
            FROM products_descriptions
            WHERE product_id = %s AND content_type = 'link' AND hyperlink IS NULL
            ORDER BY description_order
        """, (product_id,))
        return [row[0] for row in self.cursor.fetchall()]
    
    def exist_product(self, product_name):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM products WHERE product_name = %s)", (product_name,))
        return self.cursor.fetchone()[0]
    
    def exist_product_description(self, product_id):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM products_descriptions WHERE product_id = %s)", (product_id,))
        return self.cursor.fetchone()[0]

    def select_product(self, start=1, end=None):
        query="SELECT * from products WHERE product_id >= %s" + (" and product_id <= %s" if end else "")
        sele=(start, end,) if end else (start,)
        self.cursor.execute(query, sele)
        return self.cursor.fetchall()

    def make_category(self):
        for c in Data.category:
            print(self.insert_category(c), c)
        
        for parent, ca in Data.detail.items():
            for c in ca:
                print(self.insert_category(c, parent), c)
    
    def check_table(self, table_name):
        self.cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        if not self.cursor.fetchone():
            if table_name=='products': self.cursor.execute(create_products_table_query)
            else: self.cursor.execute(create_products_descriptions_table_query)
            print(f"Table '{table_name}' created successfully.")
        else:
            print(f"Table '{table_name}' already exists.")