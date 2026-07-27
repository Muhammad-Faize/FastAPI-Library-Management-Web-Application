
from fastapi import FastAPI
import Authors,Books,Borrowers,Loans,Create_table

app = FastAPI() 
Create_table.create_table()

@app.get('/')
def menu_page():
    return "Welcome to Library Management App."

@app.post('/add-author',response_model=Authors.Author)
def create_author(author:Authors.Author):
    author.add_author()
    return author
            
@app.post('/add-book',response_model=Books.Book)
def create_book(book:Books.Book):
    book.add_book()
    return book

@app.post('/add-borrower',response_model=Borrowers.Borrower)
def create_borrower(borrower:Borrowers.Borrower):
    borrower.add_borrower()
    return borrower
    
@app.post('/get-loan',response_model=Loans.Loan)
def create_loan(loan : Loans.Loan):
    loan.get_loan()
    return loan

@app.put('/return-loan')
def create_return_loan(loan_id:int):
    return Loans.Loan.return_loan(loan_id)
    
@app.get('/get-books')
def get_books():
    return Books.Book.get_books()
  
@app.get('/get-borrowed-books')
def get_borrowed_books():
    return Books.Book.get_borrowed_books()

@app.get('/get-books-by-borrower/{borrower_name}')
def get_books_by_borrower(borrower_name:str):    
    return Books.Book.get_books_by_borrower(borrower_name)    

@app.get('/get-book-advanced')
def get_book_advanced(search:str):
    return Books.Book.get_book_advanced(search)