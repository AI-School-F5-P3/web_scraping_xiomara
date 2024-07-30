# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import mysql.connector
import os

from logger import logger
from .items import QuoteItem
import db

load_dotenv()

class QuotescraperPipeline:
    
    def __init__(self):
        self.quotes_before = []
        # Realizar la conexión
        self.conn = db.Connection.get_connection()
        if self.conn.is_connected():
            db.create_tables(self.conn)
            self.cursor = self.conn.cursor()

    
    def process_item(self, item, spider):
        ''' Procesar los items.

            Hay dos tipos en el spider quotes:
            - QuoteItem
            - AuthorItem
        '''
        if isinstance(item, QuoteItem):
            # item: QuoteItem
            tags = set()
            for tag in item['tags']:
                id_tag = db.tag_get(self.conn, tag)
                if id_tag is None:
                    id_tag = db.tag_create(self.conn, tag)
                tags.add(id_tag)

            id_author = db.author_get(self.conn, item['author'])
            if id_author:
                id_quote = db.quote_create(self.conn, item)
                for id_tag in tags:
                    db.quote_tag_create(self.conn, id_quote, id_tag)
                logger.warning(f"Quote creado: {item['quote']}")
            else:
                quote = {"author": item['author'], "quote": item['quote'], "tags": tags}
                self.quotes_before.append(quote)
        else:
            # item: AuthorItem
            db.author_create(self.conn, item)
            del_author = []
            for quote in self.quotes_before:
                if item['author'] == quote['author']:
                    id_author = db.author_get(self.conn, quote['author'])
                    id_quote = db.quote_create(self.conn, 
                                               {"author": quote['author'], "quote": quote['quote']})
                    for id_tag in quote["tags"]:
                        db.quote_tag_create(self.conn, id_quote, id_tag)
                    del_author.append(quote)
            for a in del_author:
                self.quotes_before.remove(a)
        return item
    
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
