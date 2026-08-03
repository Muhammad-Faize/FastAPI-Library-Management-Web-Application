import Connection
from pydantic import Field,BaseModel,field_validator
from fastapi import HTTPException
import psycopg2
class Author(BaseModel):
    name : str = Field(min_length=2,max_length=120,description='Add author name')
    
    @field_validator('name')
    def clean_name(cls,name):
        name = name.strip().title()
        if name.isdigit():
            raise HTTPException(
                status_code=409,
                detail="The entered value cannot contain numbers")
        return name

    def add_author(self):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT name FROM Authors where name ILIKE %s''',(self.name,))
            author = cur.fetchall()
            if author:
                return f"author name '{self.name}' already exists."
            cur.execute('''INSERT INTO Authors (Name) VALUES (%s)''',(self.name,))
            con.commit()
            return "Author added sucessfully"
        except HTTPException:
            raise
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail= f"Error occured at add_author : {error}"
                )
        finally:
            if cur:
                cur.close()
            if con:
                con.close()  

    @staticmethod
    def get_auhtor():
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute("Select * FROM Authors;")
            authors = [dict(row) for row in cur.fetchall()]
            return authors
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail= f"Error occured at get_author : {error}"
                )
        
        finally:
            if cur:
                cur.close()
            if con:
                con.close() 
    @staticmethod
    def get_auhtor_by_id(id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute("Select name FROM Authors where id = %s;",(id,))
            name = cur.fetchone()
            return name['name']
       
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail= f"Error occured at get_author_by_id : {error}"
                )
        
        finally:
            if cur:
                cur.close()
            if con:
                con.close() 
    
    @staticmethod
    def delete_author(id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('DELETE FROM Authors WHERE id = %s',(id,))
            con.commit()
            return 'Author has been deleted'
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail= f"Error occured at delete_author : {error}"
                )
        
        finally:
            if cur:
                cur.close()
            if con:
                con.close()    
    @staticmethod
    def update_author(id,name):
        con = None
        cur = None
        try:
            name = name.title()
            con,cur = Connection.connection()
            cur.execute('''SELECT * FROM Authors WHERE id != %s AND NAME ILIKE %s ''',(id,name))
            if cur.fetchone():
                return f"Authors with name {name} already exists"
            cur.execute('''UPDATE Authors set name = %s where id = %s ''',(name,id))
            con.commit()
            return 'Author has been updated'

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail= f"Error occured at update_author : {error}"
                )
        
        finally:
            if cur:
                cur.close()
            if con:
                con.close()     

