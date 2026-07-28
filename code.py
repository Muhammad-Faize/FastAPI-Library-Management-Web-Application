from fastapi import Form
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
import Authors,Books,Borrowers,Loans,Create_table

app = FastAPI() 
Create_table.create_table()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def menu_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index2.html",
        context={
            "request": request
        })

@app.post('/add-author')
def create_author(name:str = Form(...)):
    try:
        author = Authors.Author(name = name)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors()) from e
    result = author.add_author()
    return {
        "success": True,
        "message": result
    }

@app.post('/add-book')
def create_book(name:str = Form(...),author_id :int = Form(...)):
    book = Books.Book(name = name,author_id=author_id)
    result = book.add_book()
    return {
        "success": True,
        "message": result
    }

@app.post('/add-borrower')
def create_borrower(name:str = Form(...)):
    try:
        borrower = Borrowers.Borrower(name = name)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors()) from e
    result = borrower.add_borrower()
    return {
        "success": True,
        "message": result
    }

@app.post('/get-loan')
def create_loan(borrower_id:int = Form(...),book_id:int = Form(...)):
    loan = Loans.Loan(borrower_id=borrower_id,book_id=book_id)
    result = loan.get_loan()
    return {
        "success": True,
        "message": result
    }

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
    data = Books.Book.get_books_by_borrower(borrower_name)    
    print(data)
    return data

@app.get('/get-book-advanced')  
def get_book_advanced(search:str):
    return Books.Book.get_book_advanced(search)