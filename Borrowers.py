import Connection
from pydantic import Field,BaseModel,field_validator

class Borrower(BaseModel):
    name : str = Field(min_length=2,max_length=120,description='Add borrower name.')
    
    @field_validator('name')
    def clean_name(cls,name):
        return name.strip().title()
    
    def add_borrower(self):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''INSERT INTO Borrowers (Name) VALUES (%s)''',(self.name,))
            con.commit()
            return 'Borrower has been added'
        except Exception as error:
            return f"Error occured at add_borrower : {error}"

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  