import Connection
from pydantic import Field,BaseModel

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
            return {"detail":f"Loan issued","status":"success"}
        except Exception as error:
            return {'status':"faliure","detail":f"error at add_loan :{error}"}

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
                    loan['book_status'] = 'Borrowed'

                else:
                    loan['book_status'] = 'Available'
            return loans
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_loan :{error}"}

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
            return {'status':"faliure","detail":f"error at get_unborrowed_book :{error}"}

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
                return {"detail":f"Loan id '{id}' doesnt exists","status":"faliure"}
            cur.execute('''SELECT 1 FROM Loans where date_returned IS Null AND id = %s ''',(id,))
            if cur.fetchone() is None:
                return {"detail":f"Loan id '{id}' is not borrowed.",'status':'faliure'}
            cur.execute('''UPDATE Loans SET date_Returned = CURRENT_TIMESTAMP where id = %s''',(id,))
            con.commit()
            return {"detail":f"Loan returned successfully",'status':'success'}
        except Exception as error:
            return {'status':"faliure","detail":f"error at return_loan :{error}"}

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
            return {"detail":f"Loan deleted successfully",'status':'success'}
        except Exception as error:
            return {'status':"faliure","detail":f"error at delete_loan :{error}"}
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
                return {}
            book_id = row['book_id']
            borrower_id = row['borrower_id']
            cur.execute('''SELECT name FROM Books where id = %s''',(book_id,))
            book_name = cur.fetchone()
            cur.execute('''SELECT name FROM Borrowers where id = %s''',(borrower_id,))
            borrower_name = cur.fetchone()
            return book_id,borrower_id,book_name['name'],borrower_name['name']
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_detail_loan :{error}"}

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
            return {"detail":f"Loan updated successfully",'status':'success'}
        except Exception as error:
            return {'status':"faliure","detail":f"error at update_loan :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
    
    @staticmethod
    def get_items_for_loan(id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()    
            cur.execute('''SELECT * FROM Borrowers''')
            borrowers = [dict(row) for row in cur.fetchall()]
            cur.execute('''
            SELECT 
                b.id AS book_id,
                b.name AS book_name
            FROM Books b
            WHERE NOT EXISTS (
                SELECT 1
                FROM Loans l
                WHERE l.book_id = b.id
                AND l.date_returned IS NULL
                AND l.id != %s
            );
        ''', (id,))            
            books = [dict(row) for row in cur.fetchall()]
            return books,borrowers
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_items_for_loan :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close() 