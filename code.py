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
#---------------------------------------------
@app.get('/get-author')
def get_author_page(request:Request):
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        'authors/get_author.html',
        {"request":request,"authors":authors}
    )
#----------------------------------------------
@app.get('/add-author-page')
def add_author_page(request:Request):
    return templates.TemplateResponse(
        request,    
        'authors/add_author.html'
    )
    
@app.post('/add-author')
def create_author(name:str = Form(...)):
    author = Authors.Author(name = name)
    return author.add_author()
#----------------------------------------------
@app.get('/delete-author-page/{id}')
def delete_author_page(request:Request,id:int):
    return templates.TemplateResponse(
        request,
        "authors/delete_author.html",
        {
            "request": request,
            "id": id
        }
    )
@app.post('/delete-author')
def delete_author(id:int = Form(...)):
    return Authors.Author.delete_author(id)
#---------------------------------------------
@app.get('/update-author-page/{id}')
def update_author_page(request:Request,id:int):
    name = Authors.Author.get_auhtor_by_id(id)
    return templates.TemplateResponse(
        request,
        "authors/update_author.html",
        {
            "request": request,
            "id": id,
            "name":name
        }
    )
@app.post('/update-author')
def update_author(id:int = Form(...),name:str = Form(...)):
    return Authors.Author.update_author(id,name)
#---------------------------------------------
@app.get("/get-borrower")
def get_borrower(request:Request):
    borrowers= Borrowers.Borrower.get_borrower()
    return templates.TemplateResponse(
        request,
        "borrowers/get_borrower.html",
        {"request":request,
        "borrowers":borrowers}
    )
#-----------------------------------------------
@app.get("/add-borrower-page")
def add_borrower_page(request:Request):
    return templates.TemplateResponse(
        request,
        "borrowers/add_borrower.html",
        {"request":request}
    )

@app.post("/add-borrower")
def add_borrower(name:str = Form(...)):
    borrower = Borrowers.Borrower(name = name)
    return borrower.add_borrower()
#------------------------------------------------
@app.get("/delete-borrower-page/{id}")
def delete_borrower_page(request:Request,id:int):
    return templates.TemplateResponse(
        request,
        "borrowers/delete_borrower.html",
        {"request":request,"id":id}
    )
    
@app.post("/delete-borrower")
def delete_borrower(id:int = Form(...)):
    return Borrowers.Borrower.delete_borrower(id)
#------------------------------------------------
@app.get("/update-borrower-page/{id}")
def update_borrower_page(request:Request,id:int):
    name = Borrowers.Borrower.get_borrower_by_id(id)
    return templates.TemplateResponse(
        request,
        "borrowers/update_borrower.html",
        {"request":request,"id":id,"name":name}
    )
    
@app.post("/update-borrower")
def update_borrower(id:int = Form(...),name:str = Form(...)):
    return Borrowers.Borrower.update_borrower(id,name)
#-------------------------------------------------- 

@app.get("/get-book")
def get_books(request:Request):
    books = Books.Book.get_book()
    return templates.TemplateResponse(
        request,
        "/books/get_book.html",
        {"request":request,"books":books}
    )
#--------------------------------------------------
@app.get("/add-book-page")
def add_book_page(request:Request):
    books = Books.Book.get_book()
    return templates.TemplateResponse(
        request,
        "books/add_book.html",
        {"request":request,"books":books}
    )
@app.post("/add-book")
def add_book(name:str = Form(...),author_id:int=Form(...)):
    book = Books.Book(name = name,author_id = author_id)
    return book.add_book()
#----------------------------------------------------
@app.get("/delete-book-page/{id}")
def delete_book_page(request:Request,id:int):
    return templates.TemplateResponse(
        request,
        "/books/delete_book.html",   
        {"request":request,"id":id}
    )
    
@app.post("/delete-book")
def delete_book(id:int = Form(...)):
    return Books.Book.delete_book(id)    
#----------------------------------------------------
@app.get("/update-book-page/{id}")
def update_book_page(request:Request,id:int):
    name = Books.Book.get_book_by_id(id)
    return templates.TemplateResponse(
        request,
        "/books/update_book.html",
        {"request":request,"id":id,"name":name}
    )
@app.post("/update-book")
def update_book(id:int = Form(...),name:str = Form(...)):
    return Books.Book.update_book(id,name)
#-------------------------------------------------------
@app.get("/get-loan")
def get_loans(request:Request):
    loans = Loans.Loan.get_loan()
    return templates.TemplateResponse(
        request,
        "/loans/get_loan.html",
        {"request":request,"loans":loans}
    )
#-------------------------------------------------------
@app.get("/add-loan-page")
def add_loan_page(request:Request):
    borrowers = Borrowers.Borrower.get_borrower()
    books = Loans.Loan.get_unborrowed_book()
    return templates.TemplateResponse(
        request,
        "loans/add_loan.html",
        {"request":request,"borrowers":borrowers,"books":books}
    )
@app.post("/add-loan")
def add_loan(borrower_id:int = Form(...),book_id:int = Form(...)):
    loan = Loans.Loan(borrower_id=borrower_id,book_id=book_id)
    return loan.add_loan()
#----------------------------------------------------------
@app.get("/return-loan-page")
def return_loan_page(request:Request):
    return templates.TemplateResponse(
        request,
        "/loans/return_loan.html",
        {"request":request}
    )
@app.post("/return-loan")
def return_loan(id:int = Form(...)):
    return Loans.Loan.return_loan(id)
#----------------------------------------------------------
@app.get("/delete-loan-page/{id}")
def delete_book_page(request:Request,id:int):
    return templates.TemplateResponse(
        request,
        "/loans/delete_loan.html",   
        {"request":request,"id":id}
    )
    
@app.post("/delete-loan")
def delete_book(id:int = Form(...)):
    return Loans.Loan.delete_loan(id)   
#-----------------------------------------------------------
@app.get("/update-loan-page/{id}")
def update_loan_page(request:Request,id:int):
    o_book,o_borrower,o_book_name,o_borrower_name = Loans.Loan.get_detail_loan(id)
    books,borrowers = Loans.Loan.get_items_for_loan()
    return templates.TemplateResponse(  
        request,
        "/loans/update_loan.html",
        {"request":request,"id":id,"o_book":o_book,"o_borrower":o_borrower,"o_book_name":o_book_name,"o_borrower_name":o_borrower_name,"borrowers":borrowers,"books":books}
    )
@app.post("/update-loan")
def update_loan(id:int=Form(...),book_id:int = Form(...),borrower_id:int = Form(...)):
    return Loans.Loan.update_loan(id,book_id,borrower_id)
