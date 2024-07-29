import pytest
from dotenv import load_dotenv
import mysql.connector
import os

import db

load_dotenv()

@pytest.fixture
def conn():
    conn = mysql.connector.connect(
        host = os.environ['DB_HOST'],
        user = os.environ['DB_USERNAME'],
        password = os.environ['DB_PASSWORD']
    )
    assert conn.is_connected(), "Error, no se puede conectar"
    db.create_tables(conn, os.environ['DB_TEST_DATABASE'])
    return conn
    # yield conn
    # cursor = conn.cursor()
    # cursor.execute("DROP DATABASE %s;", (os.environ['DB_TEST_DATABASE'],))

def test_author_create_get(conn):
    author = db.author_create(conn, {'author': 'Test', 'about': 'About test.'})
    assert author, 'Error, to create author.'
    id_obt = db.author_get(conn, 'Test')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM authors WHERE fullname='Test'")
    id_exp = cursor.fetchone()[0]
    assert id_obt == id_exp, 'Error, to get author.'

def test_tag_create_get(conn):
    tag = db.tag_create(conn, 'music')
    assert tag, 'Error, to create tag.'
    id_obt = db.tag_get(conn, 'music')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tags WHERE id = %s", (id_obt,))
    tag_obt = cursor.fetchone()[1]
    assert tag_obt == 'music', "Error, to get tag"

def test_quote_create_get(conn):
    author = {'author': 'Don Billy', 'about': 'About Billy'}
    id_author = db.author_create(conn, author)
    assert id_author, "Error, uncreated author."
    quote = {'quote': 'Eyes without a face.', 'author': 'Don Billy'}
    id_quote = db.quote_create(conn, quote)
    assert id_quote, "Error, uncreated quote."
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quotes WHERE id = %s", (id_quote,))
    result = cursor.fetchone()
    assert result[1] == quote['quote']
    assert result[2] == id_author

def test_quote_tag_create(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM quotes WHERE author_id='2'")
    id_quote = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM tags WHERE name='music'")
    id_tag = cursor.fetchone()[0]
    db.quote_tag_create(conn, id_quote, id_tag)
    cursor.execute("SELECT * FROM quotes_tags WHERE quote_id=%s", (id_quote,))
    result = cursor.fetchone()
    assert result
    assert result[1] == id_quote
    assert result[2] == id_tag

def test_fail_quote_create_get(conn):
    pass
