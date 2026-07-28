import Connection
from pydantic import Field,BaseModel
from fastapi import HTTPException

class Loan(BaseModel):
    borrower_id : int = Field(gt=0,description='Add the borrower id.')
    book_id : int = Field(gt=0,description='Add the book id.')
    def get_loan(self):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT Id FROM Borrowers where id = %s ''',(self.borrower_id,))
            if cur.fetchone() is None:
                raise HTTPException(
                    status_code= 404,
                    detail=f"Borrower with id {self.borrower_id} doesnt exists."
                )
            cur.execute('''SELECT id FROM Books where id = %s ''',(self.book_id,))
            if cur.fetchone() is None:
                raise HTTPException(
                    status_code= 404,
                    detail=f"Book with id {self.book_id} doesnt exists."
                )
            cur.execute('''
                SELECT 1
                FROM Loans
                WHERE book_id = %s
                AND date_returned IS NULL
                ''', (self.book_id,))
            if cur.fetchone() is not None:
                raise HTTPException(
                    status_code= 400,
                    detail=f"Loan already exist for such book"
                )
            cur.execute('''INSERT INTO Loans (Borrower_Id,Book_Id) VALUES (%s,%s)''',(self.borrower_id,self.book_id))
            con.commit()
            return 'Loan has been taken'

        except HTTPException:
            raise
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at add_loan : {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
    @staticmethod
    def return_loan(loan_id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT id FROM Loans where id = %s ''',(loan_id,))
            if cur.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Loan with id {loan_id} doesnt exists"
                )
            cur.execute('''SELECT 1 FROM Loans where date_returned IS Null AND id = %s ''',(loan_id,))
            if cur.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail = f"Loan with id :{loan_id} is not borrowed."
                )
            cur.execute('''UPDATE Loans SET date_Returned = CURRENT_TIMESTAMP where id = %s''',(loan_id,))
            con.commit()
            return 'Loan has been returned'
        except HTTPException:
            raise
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Error occured at return_loan : {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  