from os import device_encoding, pipe
import sqlite3
from typing import Text
import xml.etree.ElementTree as ET


# Codigo para crear la base de datos y cargar en ella la informacion del archivo categories.xml (respuesta de la api)
# de Ebay
# Por: Francisco Salazar | ciscosalazarm@gmail.com

#Create DataBase

def create_table():

    conn = sqlite3.connect('dataebay.db')
    c = conn.cursor()
    c.execute(""" CREATE TABLE categories (
        name TEXT,
        best_offer TEXT,
        auto_pay TEXT,
        level INTEGER,
        parent_id INTEGER,
        id INTEGER PRIMARY KEY,
        leaf text
        )""")
    
    conn.commit()

    conn.close()

# Insert Database
def insert_table(many_categories):

    conn = sqlite3.connect('dataebay.db')
    c = conn.cursor()

    c.executemany("INSERT OR REPLACE INTO categories VALUES (?,?,?,?,?,?,?)", many_categories)

    print("command excecuted succesfully...")

    conn.commit()

    conn.close()



def import_xml():

    trupla_categories = ()
    list_categories = []

    tree = ET.parse('categories.xml')
    root = tree.getroot()

    data = root[4]

    for category in data.iterfind('{urn:ebay:apis:eBLBaseComponents}Category'):

        best_offer = category.findtext('{urn:ebay:apis:eBLBaseComponents}BestOfferEnabled')
        auto_pay = category.findtext('{urn:ebay:apis:eBLBaseComponents}AutoPayEnabled')
        category_id = category.findtext('{urn:ebay:apis:eBLBaseComponents}CategoryID')
        category_level = category.findtext('{urn:ebay:apis:eBLBaseComponents}CategoryLevel')
        category_name = category.findtext('{urn:ebay:apis:eBLBaseComponents}CategoryName')
        category_parent_id = category.findtext('{urn:ebay:apis:eBLBaseComponents}CategoryParentID')
        leaf_category = category.findtext('{urn:ebay:apis:eBLBaseComponents}LeafCategory')

        category_id = int(category_id)
        category_level = int(category_level)
        category_parent_id = int(category_parent_id)

        trupla_categories = (category_name, best_offer, auto_pay, category_level, category_parent_id, category_id, leaf_category)
        
        list_categories.append(trupla_categories)

    insert_table(list_categories)

if __name__ == '__main__':

    create_table()
    # insert_table()
    import_xml()


