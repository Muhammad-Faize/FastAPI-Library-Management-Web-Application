import Connection
from pydantic import Field,BaseModel,field_validator

class Book(BaseModel):
    name : str = Field(min_length=2,max_length=120,description='Add book name.')
    author_id : int = Field(gt=0,description='Add the author id.')
    
    @field_validator('name')
    def clean_name(cls,name):
        return name.strip().title()
    
    def add_book(self):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT Id FROM Authors WHERE Id = %s''',(self.author_id,))
            if cur.fetchone() is None:
                return {"detail":f"Author id {self.author_id} doesnt exists","status":"faliure"}
            cur.execute('''SELECT * FROM Books WHERE name ILIKE %s''',(self.name,))
            if cur.fetchone():
                return {"detail":"Book already exists","status":"faliure"} 
            cur.execute('''INSERT INTO Books (Name,Author_Id) VALUES (%s,%s)''',(self.name,self.author_id))
            con.commit()
            return {"detail":"Book added successfully","status":"success"}

        except Exception as error:
            return {'status':"faliure","detail":f"error at add_book :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
    @staticmethod
    def get_book():    
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT Authors.id as author_id, Books.id as id, Authors.Name as author_name,Books.Name as name FROM Authors INNER JOIN Books ON Authors.Id = Books.Author_Id''')
            books = [dict(row) for row in cur.fetchall()]
            return books
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_book :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
    @staticmethod
    def delete_book(id):  
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''DELETE FROM Books where id = %s ''',(id,))
            con.commit()
            return {"detail":"Book deleted successfully","status":"success"}
        except Exception as error:
            return {'status':"faliure","detail":f"error at delete_book :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()   
    @staticmethod
    def get_book_by_id(id):  
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT name FROM Books WHERE id = %s''',(id,))
            name = cur.fetchone()
            return name['name']
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_book_by_id :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()    
    
    @staticmethod
    def update_book(id,name):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT * FROM Books WHERE id != %s AND name ILIKE %s''',(id,name))
            if cur.fetchone():
                return {"detail":f'{name} already exists',"status":"faliure"}
            cur.execute('''UPDATE Books SET name = %s WHERE id = %s ''',(name,id))
            con.commit()
            return {"detail":"Book updated successfully","status":"success"}
        except Exception as error:
            return {'status':"faliure","detail":f"error at update_book :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()           
               