import Connection
from pydantic import Field,BaseModel,field_validator

class Borrower(BaseModel):
    name : str = Field(min_length=2,max_length=120,description='Add borrower name.')
    
    @field_validator('name')
    def clean_name(cls,name):
        name = name.strip().title()
        return name
    def add_borrower(self):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            if (self.name).isdigit():
                return {"detail":"Name cannot be number","status":"faliure"}
            cur.execute('''SELECT * FROM Borrowers''')
            borrowers = [dict(row) for row in cur.fetchall()]
            for borrower in borrowers:
                if borrower['name'] == self.name:
                    return {"detail":f"borrower with name '{self.name}' already exists","status":"faliure"}
            cur.execute('''INSERT INTO Borrowers (Name) VALUES (%s)''',(self.name,))
            con.commit()
            return {"detail":f"Borrower added successfully","status":"success"}
        except Exception as error:
            return {'status':"faliure","detail":f"error at add_borrower :{error}"}
        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
    @staticmethod
    def get_borrower():
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT * FROM Borrowers ORDER BY id''')
            borrowers = [dict(row) for row in cur.fetchall()]
            return borrowers
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_borrower :{error}"}
        finally:
            if cur:
                cur.close()
            if con:
                con.close() 
    @staticmethod
    def get_borrower_by_id(id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT name FROM Borrowers WHERE id = %s''',(id,))
            name = cur.fetchone()
            return name['name']
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_borrower_by_id :{error}"}
        finally:
            if cur:
                cur.close()
            if con:
                con.close() 
    
    @staticmethod
    def delete_borrower(id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('DELETE FROM Borrowers WHERE id = %s',(id,))
            con.commit()
            return {"detail":f"Borrower deleted successfully","status":"success"}
        except Exception as error:
            if 'violates foreign key constraint' in str(error):
                return {'status':"faliure","detail":f"Borrower id {id} is issued with a loan, Hence cant be deleted"} 
            return {'status':"faliure","detail":f"error at delete_borrower :{error}"}
        finally:
            if cur:
                cur.close()
            if con:
                con.close()      
    @staticmethod
    def update_borrower(id,name):
        con = None
        cur = None
        try:
            name = name.title()
            con,cur = Connection.connection()
            cur.execute('''SELECT * FROM Borrowers WHERE id != %s AND NAME ILIKE %s ''',(id,name))
            if cur.fetchone():
                return {"detail":f"Borrower with name {name} already exists","status":"faliure"}
            cur.execute('''SELECT * FROM Loans WHERE borrower_id = %s ''',(id,))
            if cur.fetchone():
                return {'status':"faliure","detail":f"Borrower id {id} is issued with a loan, Hence cant be updated"} 
            cur.execute('''UPDATE Borrowers set name = %s where id = %s ''',(name,id))
            con.commit()
            return {"detail":f"Borrower has been updated","status":"success"}
        except Exception as error:
            return {'status':"faliure","detail":f"error at update_borrower :{error}"}
        finally:
            if cur:
                cur.close()
            if con:
                con.close()  