import Connection
from pydantic import Field,BaseModel,field_validator


class Author(BaseModel):
    name : str = Field(min_length=2,max_length=120,description='Add author name')
    
    @field_validator('name')
    def clean_name(cls,name):
        return name.strip().title()
    
    def add_author(self):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''INSERT INTO Authors (Name) VALUES (%s)''',(self.name,))
            con.commit()
            return 'Author has been added'
        except Exception as error:
            return f"Error occured at add_author : {error}"

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  