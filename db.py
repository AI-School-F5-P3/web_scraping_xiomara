from dotenv import load_dotenv
import mysql.connector
import os

from logger import logger
from quotescraper.items import AuthorItem, QuoteItem

load_dotenv()

class Connection:

    conn = None

    @classmethod
    def get_connection(cls):
        if cls.conn is None:
            try:
                logger.info("Try create database.")
                cls.conn = mysql.connector.connect(
                    host = os.environ['DB_HOST'],
                    user = os.environ['DB_USERNAME'],
                    password = os.environ['DB_PASSWORD']
                )
            except mysql.connector.Error as e:
                logger.error(e)
            else:
                logger.info("Connection database ok.")
        return cls.conn

def create_tables(conn, database=os.environ['DB_DATABASE']):
    cursor = conn.cursor()
    # database = os.environ['DB_DATABASE']
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}`;")
        logger.info("Base de datos creada.")
        cursor.execute(f"USE `{database}`;")
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
            cursor.execute(table)
            logger.info(f"Tabla creada {table.split('`')[1]}")
    except mysql.connector.Error as e:
        logger.error(e)

def author_get(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM authors WHERE fullname=%s", (name,))
    result = cursor.fetchone()
    return result[0] if result else None

def author_create(conn, item: AuthorItem):
    result = author_get(conn, item['author'])
    if result is None:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO authors(fullname, about) VALUES (%s, %s)",
                           (item['author'], item['about']))
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.DataError as e:
            logger.error(e)
    return result

def tag_get(conn, tag: str):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
    result = cursor.fetchone()
    return result[0] if result else None

def tag_create(conn, tag):
    result = tag_get(conn, tag)
    if result is None:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag,))
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.DatabaseError as e:
            logger.error(e)
    return result[0]
