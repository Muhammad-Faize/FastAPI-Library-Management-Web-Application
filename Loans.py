import Connection
from pydantic import Field,BaseModel
from fastapi import HTTPException

class Loan(BaseModel):
    borrower_id : int = Field(gt=0,description='Add the borrower id.')
    book_id : int = Field(gt=0,description='Add the book id.')
    
    def add_loan(self): 
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''INSERT INTO Loans (borrower_id,book_id) VALUES (%s,%s) ''',(self.borrower_id,self.book_id))
            con.commit()
            return 'Loan issued'
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at add_loans: {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close() 
    @staticmethod
    def get_loan():
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''    SELECT 
                                b.id as book_id, 
                                l.id as ID,
                                b.Name AS book_name,
                                br.id as borrower_id,
                                br.Name AS Borrower_Name,
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
                            ON l.Borrower_Id = br.Id 

                            WHERE l.id IS NOT NULL

                            ORDER BY l.id;
                                ''')
            loans = [dict(row) for row in cur.fetchall()]
            for loan in loans:
                if loan['date_borrowed'] is None:
                    loan['book_status'] = 'Available'

                elif loan['date_returned'] is None:
                    loan['book_status'] = 'Not Available'

                else:
                    loan['book_status'] = 'Available'
            return loans
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at get_loans: {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close() 
        
    @staticmethod
    def get_unborrowed_book():
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT *
                            FROM books b
                            WHERE NOT EXISTS (
                                SELECT 1
                                FROM loans l
                                WHERE l.book_id = b.id
                                AND l.date_returned IS NULL
                            );''')
            books = [dict(row) for row in cur.fetchall()]
            return books
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at get_loans: {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close() 
     
    @staticmethod
    def return_loan(id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT id FROM Loans where id = %s ''',(id,))
            if cur.fetchone() is None:
                return f"Loan with id {id} doesnt exists"
            cur.execute('''SELECT 1 FROM Loans where date_returned IS Null AND id = %s ''',(id,))
            if cur.fetchone() is None:
                return f"Loan with id :{id} is not borrowed."
            cur.execute('''UPDATE Loans SET date_Returned = CURRENT_TIMESTAMP where id = %s''',(id,))
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
    
    @staticmethod
    def delete_loan(id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''DELETE FROM Loans WHERE id = %s ''',(id,))
            con.commit()
            return "Loan has been deleted"
        except HTTPException:
            raise
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Error occured at delete_loan : {error}"
            )
        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
        
    @staticmethod
    def get_detail_loan(id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT book_id,borrower_id FROM Loans where id = %s''',(id,))
            row = cur.fetchone()
            if not row:
                return "Error"
            book_id = row['book_id']
            borrower_id = row['borrower_id']
            cur.execute('''SELECT name FROM Books where id = %s''',(book_id,))
            book_name = cur.fetchone()
            cur.execute('''SELECT name FROM Borrowers where id = %s''',(borrower_id,))
            borrower_name = cur.fetchone()
            return book_id,borrower_id,book_name['name'],borrower_name['name']
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at get_detail_loan : {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
    @staticmethod
    def update_loan(id,book_id,borrower_id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()    
            cur.execute('''UPDATE Loans SET borrower_id = %s , book_id = %s WHERE id = %s''',(borrower_id,book_id,id))
            con.commit()        
            return "Loan updated succesffuly"
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at update_loan : {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
    
    @staticmethod
    def get_items_for_loan():
        con = None
        cur = None
        try:
            con,cur = Connection.connection()    
            cur.execute('''SELECT * FROM Borrowers''')
            borrowers = [dict(row) for row in cur.fetchall()]
            cur.execute('''SELECT Books.id as book_id , Books.name as book_name FROM Loans FULL JOIN Books ON Loans.book_id = Books.id WHERE Loans.id IS NULL OR Loans.date_returned IS NOT NULL ;''')
            books = [dict(row) for row in cur.fetchall()]
            return books,borrowers
        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail = f"Error occured at get_items_for_loan : {error}"
            )

        finally:
            if cur:
                cur.close()
            if con:
                con.close() 