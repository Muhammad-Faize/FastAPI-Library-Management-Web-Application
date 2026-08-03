import Connection
from pydantic import Field,BaseModel,field_validator
from fastapi import HTTPException

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
                return f"Author with id {self.author_id} doesnt exists"
            cur.execute('''SELECT * FROM Books WHERE name ILIKE %s''',(self.name,))
            if cur.fetchone():
               return f"Book already exists" 
            cur.execute('''INSERT INTO Books (Name,Author_Id) VALUES (%s,%s)''',(self.name,self.author_id))
            con.commit()
            return 'Book added successfully'

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at add_book : {error}"
            )

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
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at get_books : {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
    
    @staticmethod
    @staticmethod
    def delete_book(id):  
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''DELETE FROM Books where id = %s ''',(id,))
            con.commit()
            return "Book deleted successfully"
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at delete_books : {error}"
            )

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
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at get_book_by_id : {error}"
            )

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
                return f'{name} already exists'
            cur.execute('''UPDATE Books SET name = %s WHERE id = %s ''',(name,id))
            con.commit()
            return 'Book updated succesfully'
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at update_book : {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close()           
               