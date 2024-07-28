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

load_dotenv()

class QuotescraperPipeline:
    
    def __init__(self):
        database = os.getenv('DB_DATABASE'),
        try:
            logger.info("Try create database.")
            conn = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USERNAME'),
            password = os.getenv('DB_PASSWORD')
            )
            cursor = conn.cursor()
            cursor.execute(
                f"""CREATE DATABASE IF NOT EXISTS `{database}`;
                USE {database};
                CREATE TABLE `authors` IF NOT EXISTS (
                    `id` int PRIMARY KEY AUTO INCREMENT,
                    `fullname` varchar(100),
                    `about` varchar(500)
                );

                CREATE TABLE `tags` IF NOT EXISTS (
                    `id` int PRIMARY KEY AUTO INCREMENT,
                    `name` varchar(50)
                );

                CREATEA TABLE `quotes` IF NOT EXISTS (
                    `id` int PRIMARY KEY AUTO INCREMENT,
                    `author_id` int,
                    FOREIGN KEY (author_id) REFERENCES authors(id)
                )

                CREATE TABLE `quotes_tags` IF NOT EXISTS (
                    `id` int PRIMARY KEY AUTO INCREMENT,
                    `quote_id` int,
                    `tag_id` int,
                    FOREIGN KEY (quote_id) REFERENCES quotes(id),
                    FOREIGN KEY (tag_id) REFERENCES tags(id)
                )
                """
            )
        except mysql.connector.Error as e:
            logger.error(e)
        else:
            logger.info("Create database.")
            cursor.close()
            conn.close()

    
    def process_item(self, item, spider):
        return item
