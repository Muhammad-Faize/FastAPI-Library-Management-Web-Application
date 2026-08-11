import psycopg2
import psycopg2.extras
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")

connection_pool = pool.SimpleConnectionPool(
    1,
    10,
    host=host,
    dbname=dbname,
    user=user,
    password=password,
    port=port
)


def connection():
    con = connection_pool.getconn()
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return con, cur


def release_connection(con):
    connection_pool.putconn(con)

