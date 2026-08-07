import Connection
from pydantic import Field,BaseModel,field_validator

class Book(BaseModel):
    name : str = Field(min_length=1,max_length=120,description='Add book name.')
    author_id : int = Field(gt=0,description='Add the author id.')
    quantity:int = Field(gt=-1,description='Add the quantity.')
    @field_validator('name')
    def clean_name(cls,name):
        return name.strip().title()
    
    def add_book(self):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT Id FROM Authors WHERE Id = %s''',(self.author_id,))
            if cur.fetchone() is None:
                return {"detail":f"Author id '{self.author_id}' doesnt exists","status":"faliure"}
            cur.execute('''SELECT * FROM Books WHERE name ILIKE %s AND author_id = %s''',(self.name,self.author_id))
            if cur.fetchone():
                return {"detail":"Record already exists","status":"faliure"} 
            cur.execute('''INSERT INTO Books (Name,Author_Id,Quantity) VALUES (%s,%s,%s)''',(self.name,self.author_id,self.quantity))
            con.commit()
            return {"detail":"Book added successfully","status":"success"}

        except Exception as error:
            return {'status':"faliure","detail":f"error at add_book :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
    @staticmethod
    def get_book():    
        con = None  
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT 
                                b.id,
                                b.name,
                                a.name AS author_name,
                                b.quantity,

                                -- Issued books (sum of issued_books from Loans)
                                COALESCE(SUM(l.issued_books) FILTER (WHERE l.date_returned IS NULL), 0) AS issued_books,

                                -- Remaining books
                                b.quantity - COALESCE(SUM(l.issued_books) FILTER (WHERE l.date_returned IS NULL), 0) AS remaining_books

                            FROM Books b

                            LEFT JOIN Authors a
                            ON b.author_id = a.id

                            LEFT JOIN Loans l
                            ON l.book_id = b.id

                            GROUP BY b.id, b.name, a.name, b.quantity

                            ORDER BY b.id;''')
            books = [dict(row) for row in cur.fetchall()]
            return books
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_book :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()  
    @staticmethod
    def delete_book(id):  
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''DELETE FROM Books where id = %s ''',(id,))
            con.commit()
            return {"detail":"Book deleted successfully","status":"success"}
        except Exception as error:
            if 'violates foreign key constraint' in str(error):
                return {'status':"faliure","detail":f"Book id '{id}' is issued to a loan, Hence cant be deleted"} 
            return {'status':"faliure","detail":f"error at delete_book :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()   
    @staticmethod
    def get_book_by_id(id):  
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT name,quantity FROM Books WHERE id = %s''',(id,))
            name = cur.fetchone()
            return name['name'],name['quantity']
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_book_by_id :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()    

    @staticmethod
    def get_book_by_name(book_name):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT id FROM Books WHERE name = %s''',(book_name.title(),))
            id = cur.fetchone()
            if id:
                return id['id']
            else:
                return None
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_book_by_name :{error}"}
        finally:
            if cur:
                cur.close()
            if con:
                con.close()
    @staticmethod
    def update_book(id,name,quantity):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT quantity FROM Books WHERE id = %s''',(id,))
            current_book = cur.fetchone()
            if current_book is None:
                return {"detail":f"Book id '{id}' does not exist","status":"faliure"}

            issued_books = Book.get_issued_detail(id)
            active_loans = 0
            for books in issued_books:
                active_loans += books['issued_books']
            if quantity < active_loans:
                return {"detail":f"Cannot reduce quantity to {quantity}. {active_loans} copy(ies) are still on active loan.","status":"faliure"}

            cur.execute('''SELECT * FROM Books WHERE id != %s AND name ILIKE %s''',(id,name))
            if cur.fetchone():
                return {"detail":f"'{name}' already exists","status":"faliure"}
            cur.execute('''UPDATE Books SET name = %s,quantity = %s WHERE id = %s ''',(name,quantity,id))
            con.commit()
            return {"detail":"Book updated successfully","status":"success"}
        except Exception as error:
            return {'status':"faliure","detail":f"error at update_book :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close()      
    @staticmethod
    def get_book_search(user_inp):
        con = None
        cur = None
        try:
            con, cur = Connection.connection()
            cur.execute('''
                        SELECT 
                            Authors.Name AS author_name,
                            Books.Name AS book_name,
                            Books.quantity,

                            -- Issued books (sum from Loans)
                            COALESCE(SUM(Loans.issued_books) FILTER (WHERE Loans.date_returned IS NULL), 0) AS issued_books,

                            -- Remaining books
                            Books.quantity - COALESCE(SUM(Loans.issued_books) FILTER (WHERE Loans.date_returned IS NULL), 0) AS remaining_books

                        FROM Authors

                        INNER JOIN Books 
                        ON Authors.Id = Books.Author_Id

                        LEFT JOIN Loans 
                        ON Loans.book_id = Books.id

                        WHERE Books.Name ILIKE %s

                        GROUP BY Authors.Name, Books.Name, Books.quantity

                        ORDER BY Books.Name;
            ''', (user_inp,))

            data = [dict(row) for row in cur.fetchall()]
            if data:
                return {"data": data, "status": "success"}

            return {"data": {}, "status": "failure"}
        except Exception as error:
            return {
            "data": {},
            "status": "failure",
            "detail": str(error)
            } 

        finally:
            if cur:
                cur.close()
            if con:
                con.close()   
        
    @staticmethod
    def get_issued_detail(id):   
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT 
                                br.name AS borrower_name,
                                b.name AS book_name,
                                SUM(l.issued_books) AS issued_books

                            FROM Loans l

                            JOIN Borrowers br ON l.borrower_id = br.id
                            JOIN Books b ON l.book_id = b.id

                            WHERE 
                                l.date_returned IS NULL
                                AND l.book_id = %s

                            GROUP BY br.name, b.name

                            ORDER BY br.name; ''',(id,))
            data = [dict(data) for data in cur.fetchall()]
            return data
        except Exception as error:
            return {'status':"faliure","detail":f"error at get_borrowed_books_details :{error}"}

        finally:
            if cur:
                cur.close()
            if con:
                con.close() 


