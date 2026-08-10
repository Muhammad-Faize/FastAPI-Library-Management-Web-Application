import Connection
from pydantic import Field,BaseModel

class Loan_cart(BaseModel):
    Book_Name : str = Field(min_length=1,max_length=120,description="Enter Book_name")
    Quantity : int = Field(gt=0,description="Enter quantity")

    def add_loan_cart(self):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT * FROM Loans_cart ''')
            loans = [dict(row) for row in cur.fetchall()]
            is_found = False
            for loan in loans:
                if loan['book_name'] == self.Book_Name:
                    quantity = loan['quantity'] + self.Quantity
                    cur.execute('''UPDATE Loans_cart SET quantity = %s WHERE book_name = %s''',(quantity,self.Book_Name))
                    is_found = True
            if is_found == False:
                cur.execute('''INSERT INTO Loans_cart (Book_Name, Quantity) VALUES (%s,%s)''',(self.Book_Name,self.Quantity))
            con.commit()
        except Exception as error:
            return {"status":"failure","detail":f"error at add_loan_cart: {error}"}
        finally:
            if con:
                con.close()
            if cur:
                cur.close()
    @staticmethod
    def get_loan_cart():
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''SELECT * FROM Loans_cart''')
            loan_cart = [dict(row) for row in cur.fetchall()]
            con.commit()
            return loan_cart
        except Exception as error:
            return {"status":"failure","detail":f"error at get_loan_cart: {error}"}
        finally:
            if con:
                con.close()
            if cur:
                cur.close()
    @staticmethod
    def delete_loan_cart(id):
        con = None
        cur = None
        try:
            con,cur = Connection.connection()
            cur.execute('''DELETE FROM Loans_cart WHERE Id = %s''',(id,))
            con.commit()
            return {"detail":f"Loan deleted successfully",'status':'success'} 
        except Exception as error:
            return {"status":"failure","detail":f"error at delete_loan_cart: {error}"}
        finally:
            if con:
                con.close()
            if cur:
                cur.close()

