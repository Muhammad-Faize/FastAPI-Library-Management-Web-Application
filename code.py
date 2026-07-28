from fastapi import Form
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import Authors,Books,Borrowers,Loans,Create_table

app = FastAPI() 
Create_table.create_table()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def menu_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        })

@app.post('/add-author')
def create_author(name:str = Form(...)):
    author = Authors.Author(name = name)
    author.add_author()
    return 

@app.post('/add-book')
def create_book(name:str = Form(...),author_id :int = Form(...)):
    book = Books.Book(name = name,author_id=author_id)
    book.add_book()
    return

@app.post('/add-borrower')
def create_borrower(name:str = Form(...)):
    borrower = Borrowers.Borrower(name = name)
    borrower.add_borrower()
    return

@app.post('/get-loan')
def create_loan(borrower_id:int = Form(...),book_id:int = Form(...)):
    loan = Loans.Loan(borrower_id=borrower_id,book_id=book_id)
    loan.get_loan()
    return

@app.put('/return-loan')
def create_return_loan(loan_id:int = Form(...)):
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