import pytest
from db import Connection

def test_connection():
	db = Connection()
	db.get_connection()
	assert db.conn.is_connected(), "Error, no se puede conectar"

def test_create_tables():
	pass

def test_author_create():
	pass