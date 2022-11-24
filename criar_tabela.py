import sqlite3

# criar instancia de conexão com o banco
connection = sqlite3.connect('records.db')
# inicializar cursor
cursor = connection.cursor()

# IF PARA CRIAR SE NAO TIVER CRIADO
create_table = "CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, pontos int)"

cursor.execute(create_table)

connection.commit()
connection.close()
