import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('host')
dbname = os.getenv('dbname')
user = os.getenv('user')
password = os.getenv('password')
port = os.getenv('port')

def connection():
    con = psycopg2.connect(
        host = host,
        dbname = dbname,
        user = user,
        password = password,
        port = port
    )
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return con ,cur