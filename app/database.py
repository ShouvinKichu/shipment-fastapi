import sqlite3

connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

# create a table
cursor.execute(
    "CREATE TABLE IF NOT EXISTS shipment (id INTEGER PRIMARY KEY, content TEXT, weight REAL, status TEXT)"
)

# cursor.execute("DROP TABLE shipment")
# connection.commit()

# add shipment data
# cursor.execute("""
#     INSERT INTO shipment
#     VALUES(12701, 'creatine', 1, 'In_Transit')
# """)
# connection.commit()

# update a data
cursor.execute("""
    UPDATE shipment SET status = 'delivered' WHERE id = 12701
""")
connection.commit()

# reading a data
# cursor.execute("""
#     SELECT * FROM shipment WHERE id = 12702
# """)
# result = cursor.fetchone()
# print(result)

# delete a data
# cursor.execute("""
#     DELETE FROM shipment WHERE id = 12703
# """)
# connection.commit()



connection.close()