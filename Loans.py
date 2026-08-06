import Connection
from pydantic import Field,BaseModel

class Loan(BaseModel):
    borrower_id : int = Field(gt=0,description='Add the borrower id.')
    book_id : int = Field(gt=0,description='Add the book id.')
    issued_books:int = Field(gt=0,description="Add issued books")
    
    def add_loan(self): 
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT quantity FROM Books WHERE id = %s''',(self.book_id,))
            book = cur.fetchone()
            if book is None:
                return {"detail":f"Book id '{self.book_id}' does not exist","status":"faliure"}

            cur.execute('''SELECT COUNT(*) AS active_count FROM Loans WHERE book_id = %s AND date_returned IS NULL''',(self.book_id,))
            active_count = cur.fetchone()['active_count']
            if active_count >= book['quantity']:
                return {"detail":f"Book id '{self.book_id}' is not available for loan. All {book['quantity']} copies are currently borrowed.","status":"faliure"}
            cur.execute('''INSERT INTO Loans (borrower_id,book_id,issued_books) VALUES (%s,%s,%s) ''',(self.borrower_id,self.book_id,self.issued_books))
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
                                l.id AS id,
                                b.id AS book_id,
                                b.Name AS book_name,
                                br.id AS borrower_id,
                                br.Name AS borrower_name,
                                l.Date_Borrowed,
                                l.Date_Returned,
                                l.issued_books,
                                l.book_status

                            FROM Loans l
                            JOIN Books b ON l.book_id = b.id
                            JOIN Borrowers br ON l.borrower_id = br.id

                            ORDER BY (l.Date_Returned IS NULL) DESC, l.id;
                                ''')
            loans = [dict(row) for row in cur.fetchall()]
            for loan in loans:
                if loan['date_borrowed'] is None:
                    loan['book_status'] = 'Returned'

                elif loan['date_returned'] is None:
                    loan['book_status'] = 'Active'

                else:
                    loan['book_status'] = 'Returned'
            cur.execute('''TRUNCATE TABLE Loans_cart ''')
            con.commit()
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
            cur.execute('''SELECT b.id, b.name, b.quantity
                            FROM books b
                            LEFT JOIN (
                                SELECT book_id, COUNT(*) AS active_count
                                FROM loans
                                WHERE date_returned IS NULL
                                GROUP BY book_id
                            ) active ON active.book_id = b.id
                            WHERE COALESCE(active.active_count, 0) < b.quantity;''')
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
            cur.execute('''SELECT book_id,borrower_id,issued_books FROM Loans where id = %s''',(id,))
            row = cur.fetchone()
            if not row:
                return {}
            book_id = row['book_id']
            borrower_id = row['borrower_id']
            issued_books = row['issued_books']
            cur.execute('''SELECT name FROM Books where id = %s''',(book_id,))
            book_name = cur.fetchone()
            cur.execute('''SELECT name FROM Borrowers where id = %s''',(borrower_id,))
            borrower_name = cur.fetchone()
            return book_id,borrower_id,book_name['name'],borrower_name['name'],issued_books
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_detail_loan :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
    @staticmethod
    def update_loan(id,book_id,borrower_id,issued_books):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()    
            cur.execute('''UPDATE Loans SET borrower_id = %s , book_id = %s,issued_books = %s WHERE id = %s''',(borrower_id,book_id,issued_books,id))
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
            LEFT JOIN (
                SELECT book_id, COUNT(*) AS active_count
                FROM Loans
                WHERE date_returned IS NULL
                AND id != %s
                GROUP BY book_id
            ) active ON active.book_id = b.id
            WHERE COALESCE(active.active_count, 0) < b.quantity;
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
    
    @staticmethod
    def get_available_books(book):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT 
                            (b.quantity - COALESCE(SUM(l.issued_books) 
                                FILTER (WHERE l.date_returned IS NULL), 0)
                            ) AS remaining_quantity

                        FROM Books b

                        LEFT JOIN Loans l 
                            ON b.id = l.book_id

                        WHERE b.id = %s

                        GROUP BY b.id, b.quantity;''',(book ,))    
            quantity = dict(cur.fetchone())
            return quantity
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_available_books :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close() 
