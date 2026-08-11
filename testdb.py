from Connection import connection

con, cur = connection()

cur.execute("SELECT version();")
result = cur.fetchone()

print(result)

cur.close()
con.close()