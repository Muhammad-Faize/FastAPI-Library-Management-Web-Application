import Connection
from pydantic import Field,BaseModel,field_validator,EmailStr
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated = "auto")

Admin_Email = ["mfaize06@gmail.com"]

class User(BaseModel):
    username:str = Field(min_length=1,max_length=255,description="Enter username.")
    email:EmailStr = Field(description="Enter email.")
    password:str = Field(min_length=1,max_length=72,description="Enter password.")
    
    @field_validator('username')
    def clean_username(cls, username):
        return username.strip().lower()    
    
    def register(self):
        cur = None
        con = None
        try:
            con ,cur = Connection.connection()
            if (self.username).isdigit():
                return {"status":"failure","detail":"Username must contain alphabets."}
            cur.execute('''SELECT * FROM Users WHERE username = %s ''',(self.username,))
            if cur.fetchone():
                return {"status":"failure","detail":"username is taken"}
            cur.execute('''SELECT * FROM Users WHERE email = %s ''',(self.email.lower(),))
            if cur.fetchone():
                return {"status":"failure","detail":"Email is already registered"}
            hashed_password = pwd_context.hash(self.password)
            if self.email.lower() not in Admin_Email:
                role_id = User.get_role_id('user')['id']
            else:
                role_id = User.get_role_id('admin')['id']
            cur.execute('''INSERT INTO Users (username,email,hashed_password,role_id) VALUES (%s,%s,%s,%s)''',(self.username.lower(),self.email.lower(),hashed_password,role_id))
            con.commit()
            return {"status":"success","detail":"Account is registered"}
        except Exception as error:
            return {"status":'faliure',"detail":f"error occured at register:{error}"}
        finally:
            if cur:
                cur.close()
            if con:
                Connection.release_connection(con)
    @staticmethod
    def get_role_id(role):
        cur = None
        con = None
        try:
            con ,cur = Connection.connection()
            cur.execute('''SELECT Id FROM Roles where role ILike %s''',(role,))
            return dict(cur.fetchone())
        except Exception as error:
            return {"status":'faliure',"detail":f"error occured at get_user:{error}"}
        finally:
            if cur:
                cur.close()
            if con:
                Connection.release_connection(con)          
    
    @staticmethod
    def get_user():
        cur = None
        con = None
        try:
            con ,cur = Connection.connection()
            cur.execute('''SELECT Users.id,Users.username,Users.email,Roles.role FROM Users JOIN Roles ON Users.role_id = Roles.id''')
            users = [dict(row) for row in cur.fetchall()]
            return users
        except Exception as error:
            return {"status":'faliure',"detail":f"error occured at get_user:{error}"}
        finally:
            if cur:
                cur.close()
            if con:
                Connection.release_connection(con)                 
    
    @staticmethod
    def delete_user(id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('DELETE FROM Users WHERE id = %s',(id,))
            con.commit()
            return {"detail":'User deleted successfully',"status":"success"}
        except Exception as error: 
            return {'status':"failure","detail":f"error at delete_user :{error}"}    
        
        finally:
            if cur:
                cur.close()
            if con:
                Connection.release_connection(con) 
    
    def get_user_detail(id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT username,email,hashed_password FROM Users WHERE Id = %s ''',(id,))
            data = [dict(row) for row in cur.fetchall()]
            return data
        except Exception as error: 
            return {'status':"failure","detail":f"error at get_user_detail :{error}"}    
        
        finally:
            if cur:
                cur.close()
            if con:
                Connection.release_connection(con)         
    
    def update_user(id,username,email,password):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            users = User.get_user()
            for user in users:
                if user['id'] == id:
                    continue
                if user['username'] == username.lower():
                    return {'status':"failure","detail":"Username already exists"}
            if username.isdigit():
                return {"status":"failure","detail":"Username must contain alphabets."}
            data = User.get_user_detail(id)
            if not (password.strip()):
                password = data[0]['hashed_password']
            else:
                password = pwd_context.hash(password)
            cur.execute('''UPDATE Users SET username = %s, email = %s, hashed_password = %s WHERE Id = %s ''',(username.lower(),email.lower(),password,id))
            con.commit()
            return {'status':"success",'detail':"User updated successfully."}
        except Exception as error: 
            return {'status':"failure","detail":f"error at update_user :{error}"}    
        
        finally:
            if cur:
                cur.close()
            if con:
                Connection.release_connection(con)        
    
    @staticmethod    
    def login(username,password):
        cur = None
        con = None
        try:
            con ,cur = Connection.connection()
            cur.execute('''SELECT * FROM Users WHERE username = %s''',(username.lower(),))
            row = cur.fetchone()
            if not row:
                return {"status":"failure","detail":"Invalid username or password"}
            if not pwd_context.verify(password,row['hashed_password']):
                return {"status":"failure","detail":"Invalid username or password"}
            cur.execute('''SELECT Role FROM Roles WHERE id = %s''',(row['role_id'],))
            role = dict(cur.fetchone())['role']
            return {
                "status":"success",
                "detail":"Login successful",
                "username": row['username'],
                "role": role
            }
        except Exception as error:
            return {"status":'faliure',"detail":f"error occured at login:{error}"}
        finally:
            if cur:
                cur.close()
            if con:
                Connection.release_connection(con)
                