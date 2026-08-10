import Connection
from pydantic import Field,BaseModel,field_validator

class Author(BaseModel):
    name : str = Field(min_length=1,max_length=120,description='Add author name')
    
    @field_validator('name')
    def clean_name(cls,name):
        name = name.strip().title()
        return name

    def add_author(self):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT * FROM Authors WHERE name = %s ''',(self.name,))
            if cur.fetchone():
                return {"detail":"Author already exists","status":"failure"}
            if (self.name).isdigit():
                return {"detail":"Name cannot be a number","status":"failure"}
            cur.execute('''INSERT INTO Authors (Name) VALUES (%s)''',(self.name,))
            con.commit()
            return {"detail":"Author added sucessfully","status":"success"}
        except Exception as error:
            return {'status':"failure","detail":f"error at add_author :{error}"}
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
            return {'status':"failure","detail":f"error at get_author :{error}"}    
        finally:
            if cur:
                cur.close()
            if con:
                con.close() 
                
    @staticmethod
    def get_auhtor_by_name(author_name):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute("Select id FROM Authors where name = %s;",(author_name.title(),))
            id = cur.fetchone()
            if id:
                return id['id']
            return None
        except Exception as error:
            return {'status':"failure","detail":f"error at add_author_by_name :{error}"}
        
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
            return {'status':"failure","detail":f"error at add_author_by_id :{error}"}
        
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
            return {"detail":'Author deleted successfully',"status":"success"}
        except Exception as error:
            if 'violates foreign key constraint' in str(error):
                return {'status':"failure","detail":f"Author is issued with a book, Hence cant be deleted"}    
            return {'status':"failure","detail":f"error at delete_author :{error}"}    
        
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
            if name.isdigit():
                return {"detail":"Name cannot be a number","status":"failure"}
            con,cur = Connection.connection()
            cur.execute('''SELECT * FROM Authors WHERE id != %s AND NAME ILIKE %s ''',(id,name))
            if cur.fetchone():
                return {"detail":f"Author name '{name}' already exists","status":"failure"}
            cur.execute('''UPDATE Authors set name = %s where id = %s ''',(name,id))
            con.commit()
            return {"detail":'Author updated successfully',"status":"success"}

        except Exception as error:
            return {'status':"failure","detail":f"error at update_author :{error}"}
        
        finally:
            if cur:
                cur.close()
            if con:
                con.close()     

    @staticmethod
    def search_author(search):
        con = None
        cur = None
        try:
            search = search.title()
            con,cur = Connection.connection()
            cur.execute('''SELECT * from Authors where name Ilike %s''',(f"%{search}%",))
            row = cur.fetchall()
            if row:
                return [dict(data) for data in row]
            else:
                return None
        except Exception as error:
            return {'status':"failure","detail":f"error at search_author :{error}"}
        
        finally:
            if cur:
                cur.close()
            if con:
                con.close() 