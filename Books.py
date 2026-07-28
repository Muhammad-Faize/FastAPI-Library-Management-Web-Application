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
            cur.execute('''SELECT Id FROM Authors where Id = %s''',(self.author_id,))
            if cur.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Author with id {self.author_id} doesnt exists"
                )
            cur.execute('''INSERT INTO Books (Name,Author_Id) VALUES (%s,%s)''',(self.name,self.author_id))
            con.commit()
            return 'Book has been added'
        
        except HTTPException:
            raise
        
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
    def get_books():    
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT Authors.Name as Author_Name,Books.Name as Book_Name FROM Authors INNER JOIN Books ON Authors.Id = Books.Author_Id''')
            data = [dict(row) for row in cur.fetchall()]
            if len(data) == 0:
                return 'No record exists'
            return data
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
    def get_borrowed_books():
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''    SELECT 
                                b.Id AS Book_Id,
                                b.Name AS Book_Name,
                                br.Name AS Last_Borrower,
                                l.Date_Borrowed,
                                l.Date_Returned

                                FROM Books b

                                LEFT JOIN Loans l
                                ON l.Id = (
                                    SELECT MAX(Id)
                                    FROM Loans
                                    WHERE book_id = b.Id
                                )

                                LEFT JOIN Borrowers br
                                ON l.Borrower_Id = br.Id;
                                ''')
            data = [dict(row) for row in cur.fetchall()]
            if len(data) == 0:
                return 'no record exists'
            for loan in data:
                if loan['date_borrowed'] is None:
                    loan['book_status'] = 'Available'

                elif loan['date_returned'] is None:
                    loan['book_status'] = 'Not Available'

                else:
                    loan['book_status'] = 'Available'
            return data
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at get_borrowed_books : {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close()     
    @staticmethod
    def get_books_by_borrower(borrower_name):    
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            borrower_name = borrower_name.title()
            cur.execute('''SELECT Loans.Id as Loan_Id, Borrowers.Name as Borrower_Name ,Loans.Book_Id,Loans.Date_Borrowed,Loans.Date_Returned FROM Borrowers JOIN Loans ON Borrowers.Id = Loans.Borrower_Id WHERE Borrowers.Name ILIKE %s AND date_returned is null''',(f"%{borrower_name}%",))
            data = [dict(row) for row in cur.fetchall()]
            if len(data) >= 1:
                return data
            else:
                return []

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at get_books_by_borrower : {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close()   
    @staticmethod
    def get_book_advanced(user_inp):
        con = None
        cur = None
        try:
            if not user_inp.strip():
                return []   
            con,cur = Connection.connection()
            cur.execute('''SELECT Authors.Name as Author_Name,Books.Name as Book_Name FROM Authors INNER JOIN Books ON Authors.Id = Books.Author_Id WHERE Authors.Name ILIKE %s OR Books.Name ILIKE %s''',(f"%{user_inp.title()}%",f"%{user_inp.title()}%"))
            data = [dict(row) for row in cur.fetchall()]
            if len(data) >= 1:
                return data
            else:
                return []
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at get_book_advance : {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  