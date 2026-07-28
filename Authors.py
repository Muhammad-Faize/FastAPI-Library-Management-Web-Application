import Connection
from pydantic import Field,BaseModel,field_validator
from fastapi import HTTPException

class Author(BaseModel):
    name : str = Field(min_length=2,max_length=120,description='Add author name')
    
    @field_validator('name')
    def clean_name(cls,name):
        name = name.strip().title()
        if not name:
            raise ValueError("Name cannot be empty")
        if name.isdigit():
            raise ValueError("The entered value cannot contain numbers")
        return name

    def add_author(self):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''INSERT INTO Authors (Name) VALUES (%s)''',(self.name,))
            con.commit()
            return 1
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