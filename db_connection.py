import sqlite3


def init():
	connection = sqlite3.connect("database.db")

	sqlite3_create_table_queary = """
	CREATE TABLE IF NOT EXISTS pizza (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL UNIQUE,
	ingredients TEXT NOT NULL UNIQUE,
	price INTEGER NOT NULL);"""

	cursor = connection.cursor()
	cursor.execute(sqlite3_create_table_queary)
	connection.commit()
	connection.close()
	print("Table close")

init()


def get_db_connection():
	connection = sqlite3.connect("database.db", timeout=10) # timeout - закрывает бд если ее не использовали сам через время 
	connection.row_factory = sqlite3.Row
	return connection


def get_pizza(pizza_id):
	connection = get_db_connection()
	select_query = "SELECT * FROM pizza WHERE id=?"
	pizza = connection.execute(select_query, (pizza_id,)).fetchone()
	connection.close()
	return pizza


def create(name, ingredients, price):
    connection = get_db_connection()
    create_query = "INSERT INTO pizza (name, ingredients, price) VALUES (?, ?, ?)"
    index = connection.execute(create_query, (name, ingredients, price)).lastrowid
    connection.commit()
    connection.close()
    return index


def update(pizza_id, name, ingredients, price):
   connection = get_db_connection()
   connection.execute("UPDATE pizza SET name=?, ingredients=?, price=? WHERE id=?",
                      (name, ingredients, price, pizza_id))
   connection.commit()
   connection.close()
   return 202


def delete(pizza_id):
   connection = get_db_connection()
   connection.execute('DELETE FROM pizza WHERE id = ?', (pizza_id,))
   connection.commit()
   connection.close()
   return 200


def get_all_pizzas():
    connection = get_db_connection()
    select_query = "SELECT * FROM pizza"
    pizzas = connection.execute(select_query).fetchall()
    connection.close()
    return pizzas
