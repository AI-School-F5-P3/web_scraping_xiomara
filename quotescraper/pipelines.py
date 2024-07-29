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
from .items import AuthorItem, QuoteItem

load_dotenv()

class QuotescraperPipeline:
    
    def __init__(self):
        self.quotes_before = {}
        database = os.environ['DB_DATABASE']
        try:
            logger.info("Try create database.")
            self.conn = mysql.connector.connect(
            host = os.environ['DB_HOST'],
            user = os.environ['DB_USERNAME'],
            password = os.environ['DB_PASSWORD']
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}`;")
            logger.info(f"Create database: {database}")
            self.cursor.execute(f"USE `{database}`;")
            tables = [
                """
                CREATE TABLE IF NOT EXISTS `authors` (
                    `id` int PRIMARY KEY AUTO_INCREMENT,
                    `fullname` varchar(100),
                    `about` varchar(3000)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `tags` (
                    `id` int PRIMARY KEY AUTO_INCREMENT,
                    `name` varchar(50)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `quotes` (
                    `id` int PRIMARY KEY AUTO_INCREMENT,
                    `quote` varchar (500),
                    `author_id` int,
                    FOREIGN KEY (author_id) REFERENCES authors(id)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `quotes_tags` (
                    `id` int PRIMARY KEY AUTO_INCREMENT,
                    `quote_id` int,
                    `tag_id` int,
                    FOREIGN KEY (quote_id) REFERENCES quotes(id),
                    FOREIGN KEY (tag_id) REFERENCES tags(id)
                );
                """
            ]
            for table in tables:
                self.cursor.execute(table)
                logger.info(f"Tabla creada {table.split('`')[1]}")

        except mysql.connector.Error as e:
            logger.error(e)
        else:
            logger.info("Create database.")
            # self.cursor.close()
            # self.conn.close()

    
    def process_item(self, item, spider):
        if isinstance(item, QuoteItem):
            tags = set()
            for tag in item['tags']:
                self.cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
                result = self.cursor.fetchone()
                id_tag = result[0] if result else None
                logger.info(f"tag: ------{id_tag}")
                if id_tag is None:
                    self.cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag,))
                    self.conn.commit()
                    id_tag = self.cursor.lastrowid
                tags.add(id_tag)

            self.cursor.execute("SELECT id FROM authors WHERE fullname=%s", (item['author'],))
            result = self.cursor.fetchone()
            author = result[0] if result else None
            if author:
                self.cursor.execute("INSERT INTO quotes (quote, author_id) VALUES (%s, %s)", (item['quote'], author))
                self.conn.commit()
                id_quote = self.cursor.lastrowid
                for id_tag in tags:
                    self.cursor.execute("INSERT INTO quotes_tags VALUES (%s, %s)", (id_quote, id_tag))
                logger.warning("Quote creado.")
            else:
                self.quotes_before[author] = {"quote": item['quote'], "tags": tags}
        else:
            self.cursor.execute("INSERT INTO authors(fullname, about) VALUES (%s, %s)", (item['author'], item['about']))
            self.conn.commit()
            id_quote = self.cursor.lastrowid
            for author in self.quotes_before.keys():
                if item['author'] == author:
                    self.cursor.execute(f"SELECT id FROM authors WHERE fullname={item['author']}")
                    id_author = self.cursor.fetchone()[0]
                    self.cursor.execute("INSERT INTO quotes(quote, author_id) VALUES (%s, %s)", (author['quote'], id_author))
                    for id_tag in author['tags']:
                        self.cursor.execute("INSERT INTO quotes_tags VALUES (%s, %s)", (id_quote, id_tag))
                    del self.quotes_before[author]
        return item
    
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
