# connect_db.py
# 01_create_db.py
import sqlite3
import datetime


# inserindo dados na tabela
# cursor.execute("""
# INSERT INTO STATISTICS (result, timestamp)
# VALUES ( ?, ?)
# """, ('blassasadasasasasas', datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
# )

# # gravando no bd
# conn.commit()


# # lendo os dados
# cursor.execute("""
# SELECT * FROM STATISTICS;
# """)

# for linha in cursor.fetchall():
#     print(linha)



def insert_statistics(result, time_spent):

	conn = sqlite3.connect('database.db')

	cursor = conn.cursor()

	#inserindo dados na tabela
	cursor.execute("""
	INSERT INTO STATISTICS (result, time_spent)
	VALUES (?, ?)
	""", (result, time_spent)
	)

	conn.commit()

	conn.close()



def get_statistics():
	conn = sqlite3.connect('database.db')

	cursor = conn.cursor()
	stats = []

	cursor.execute("""
	SELECT * FROM STATISTICS;
	""")

	for linha in cursor.fetchall():
		stats.append((linha[0], linha[1]))


	# excluindo os dados da tabela
	cursor.execute("""
	DELETE FROM STATISTICS
	""")

	conn.commit()


	conn.close()

	return stats




if __name__ == "__main__":

	# # criando a tabela (schema)

	# conn = sqlite3.connect('database.db')

	# cursor = conn.cursor()

	# cursor.execute("""
	# CREATE TABLE STATISTICS (
	#         result TEXT,
	#         time_spent INTEGER       
	# );
	# """)

	# conn.close()

	insert_statistics("teste1", 10)

	stats = get_statistics()

	print stats

	#print stats


