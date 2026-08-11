import Connection,os

def create_table():
    con = None
    cur = None
    try:
        con,cur = Connection.connection()
        folder = os.path.dirname(os.path.abspath(__file__))
        files = ['script.sql']
        for file in files:
            file_path = os.path.join(folder,file)
            with open(file_path,'r') as file:
                script = file.read()
                cur.execute(script)
                con.commit()
        print("Tables were created.")
    except Exception as error:
        print(f"error occured at creat table :{error}")
    finally:
        if cur:
            cur.close()
        if con:
            Connection.release_connection(con)  