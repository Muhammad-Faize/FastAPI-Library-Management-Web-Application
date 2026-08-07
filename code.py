from fastapi import Form
from fastapi import FastAPI, Request,Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import Authors,Books,Borrowers,Loans,Create_table,Loans_cart

app = FastAPI() 
Create_table.create_table()

app.mount("/static", StaticFiles(directory="static"), name="static")

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
def add_author(request:Request,name:str = Form(...)):
    author = Authors.Author(name = name)
    msg = author.add_author()
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        "authors/get_author.html",
        {"request":request,"authors":authors,"msg":msg}
    )
#----------------------------------------------
@app.get('/delete-author/{id}')
def delete_author(request:Request,id:int):
    msg = Authors.Author.delete_author(id)
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        "authors/get_author.html",
        {"request":request,"authors":authors,"msg":msg}
    )
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
def update_author(request:Request,id:int = Form(...),name:str = Form(...)):
    msg = Authors.Author.update_author(id,name)
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        "authors/get_author.html",
        {"request":request,"authors":authors,"msg":msg}
    )    
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
def add_borrower(request:Request,name:str = Form(...)):
    borrower = Borrowers.Borrower(name = name)
    msg = borrower.add_borrower()
    borrowers = Borrowers.Borrower.get_borrower()
    return templates.TemplateResponse(
        request,
        "borrowers/get_borrower.html",
        {"request":request,"borrowers":borrowers,"msg":msg}
    ) 

#------------------------------------------------  
@app.get("/delete-borrower/{id}")
def delete_borrower(request:Request,id:int):
    msg = Borrowers.Borrower.delete_borrower(id)
    borrowers = Borrowers.Borrower.get_borrower()
    return templates.TemplateResponse(
        request,
        "borrowers/get_borrower.html",
        {"request":request,"borrowers":borrowers,"msg":msg}
    ) 
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
def update_borrower(request:Request,id:int = Form(...),name:str = Form(...)):
    msg = Borrowers.Borrower.update_borrower(id,name)
    borrowers = Borrowers.Borrower.get_borrower()
    return templates.TemplateResponse(
        request,
        "borrowers/get_borrower.html",
        {"request":request,"borrowers":borrowers,"msg":msg}
    ) 
#-------------------------------------------------- 
@app.get("/get-borrower-details/{id}")
def get_borrower_detail(request:Request,id:int):
    borrower_books,borrower = Borrowers.Borrower.get_borrower_details(id)
    return templates.TemplateResponse(
        request,
        'borrowers/get_borrower_details.html',
        {'request':request,'id':id,'borrower_books':borrower_books,'borrower':borrower}
    )
#-------------------------------------------------------------
@app.get('/get-borrower-search')
def get_borrower_search(request: Request, search: str):  
    borrower,borrowed_books,status = Borrowers.Borrower.get_borrower_search(search)
    return templates.TemplateResponse(
        request,
        "borrowers/get_borrower_search.html",
        {
            "request": request,
            "borrower": borrower,
            'borrowed_books':borrowed_books,
            "status": status
        }
    )
#--------------------------------------------------
@app.get("/get-book")
def get_books(request:Request):
    books = Books.Book.get_book()
    return templates.TemplateResponse(
        request,
        "books/get_book.html",
        {"request":request,"books":books}
    )
#--------------------------------------------------
@app.get("/add-book-page")
def add_book_page(request:Request):
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        "books/add_book.html",
        {"request":request,"books":authors,"name":"","quantity":"","search":""}
    )
@app.post("/add-book")
def add_book(request:Request,name:str = Form(...),author_id:int=Form(...),quantity:int=Form(...),search:str =Form(default="")):
    if author_id == 0:
        results = Authors.Author.search_author(search)
        if results:
            msg = {"detail":"Please select an author before adding the book.","status":"failure"}
            return templates.TemplateResponse(
                request,
                "books/add_book.html",
                {"request":request,"results":results,"search":search,"name":name,"quantity":quantity,"msg":msg}
            )
        author = Authors.Author(name=search)
        msg_author = author.add_author()
        if msg_author.get("status") != "success":
            return templates.TemplateResponse(
                request,
                "books/add_book.html",
                {"request":request,"results":None,"search":search,"name":name,"quantity":quantity,"msg":msg_author}
            )
        new_author_id = Authors.Author.get_auhtor_by_name(search)
        if new_author_id is None:
            msg = {"detail":"Failed to retrieve newly created author.","status":"failure"}
            return templates.TemplateResponse(
                request,
                "books/add_book.html",
                {"request":request,"results":None,"search":search,"name":name,"quantity":quantity,"msg":msg}
            )
        author_id = new_author_id
    book = Books.Book(name = name,author_id = author_id,quantity=quantity)
    msg = book.add_book()
    books = Books.Book.get_book()
    return templates.TemplateResponse(
        request,
        "books/get_book.html",
        {"request":request,"books":books,"msg":msg}
    ) 
#----------------------------------------------------
@app.get("/delete-book/{id}")
def delete_book(request:Request,id:int):
    msg = Books.Book.delete_book(id)
    books = Books.Book.get_book()
    return templates.TemplateResponse(
        request,
        "books/get_book.html",
        {"request":request,"books":books,"msg":msg}
    ) 
#----------------------------------------------------
@app.get("/update-book-page/{id}")
def update_book_page(request:Request,id:int):
    name,quantity = Books.Book.get_book_by_id(id)
    return templates.TemplateResponse(
        request,
        "books/update_book.html",
        {"request":request,"id":id,"name":name,"quantity":quantity}
    )
@app.post("/update-book")
def update_book(request:Request,id:int = Form(...),name:str = Form(...),quantity:int=Form(...)):
    msg = Books.Book.update_book(id,name,quantity)
    books = Books.Book.get_book()
    return templates.TemplateResponse(
        request,
        "books/get_book.html",
        {"request":request,"books":books,"msg":msg}
    ) 
#-------------------------------------------------------------
@app.get('/get-book-search')
def get_book_search(request: Request, search: str):  
    books = Books.Book.get_book_search(search)
    return templates.TemplateResponse(
        request,
        "books/get_book_search.html",
        {
            "request": request,
            "books": books['data'],
            "status": books["status"]
        }
    )
@app.post('/search-author')
def search_author(request:Request,search:str=Form(...),name:str=Form(default=""),quantity:int=Form(default=0)):
    results = Authors.Author.search_author(search)
    return templates.TemplateResponse(
        request,
        "books/add_book.html",
        {"request":request,"results":results,'search':search,'name':name,'quantity':quantity}
    )
@app.get('/get-issued-detail/{id}')
def get_issued_detail(request:Request,id:int):
    data = Books.Book.get_issued_detail(id)
    return templates.TemplateResponse(
        request,
        "books/get_issued_detail.html",
        {"request":request,"data":data}
    )
#-------------------------------------------------------
@app.get("/get-loan")
def get_loans(request: Request, page: int = 1, limit: int = 10):

    offset = (page - 1) * limit

    loans = Loans.Loan.get_loan(limit, offset)
    total_loans = Loans.Loan.count_loans()

    total_pages = (total_loans + limit - 1) // limit

    return templates.TemplateResponse(
        request,
        "loans/get_loan.html",
        {
            "request": request,
            "loans": loans,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
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
def add_loan(request:Request,borrower_name:str=Form(...)):
    borrower_id = Borrowers.Borrower.get_borrower_by_name(borrower_name)
    loan_cart = Loans_cart.Loan_cart.get_loan_cart()
    for loan in loan_cart:
        book_name = loan['book_name']
        quantity = loan['quantity']
        book_id = Books.Book.get_book_by_name(book_name)
        if borrower_id is None:
            msg = {"detail":"Borrower not exists","status":"failure"}
            borrowers = Borrowers.Borrower.get_borrower()
            books = Loans.Loan.get_unborrowed_book()
            return templates.TemplateResponse(
                request,
                "loans/add_loan.html",
                {"request":request,"borrowers":borrowers,"books":books,"loan_cart":loan_cart,"msg":msg}
            )
        elif book_id is None:
            msg = {"detail":"Book not exists","status":"failure"}
            borrowers = Borrowers.Borrower.get_borrower()
            books = Loans.Loan.get_unborrowed_book()
            return templates.TemplateResponse(
                request,
                "loans/add_loan.html",
                {"request":request,"borrowers":borrowers,"books":books,"loan_cart":loan_cart,"msg":msg}
            )
        else: 
                available = Loans.Loan.get_available_books(book_id)['remaining_quantity']
                if available >= quantity:
                    loan = Loans.Loan(borrower_id=borrower_id,book_id=book_id,issued_books = quantity)
                    msg = loan.add_loan()
                    page = 1
                    limit = 10
                    offset = (page - 1) * limit

                    loans = Loans.Loan.get_loan(limit, offset)
                    total_loans = Loans.Loan.count_loans()
                    total_pages = (total_loans + limit - 1) // limit

                    return templates.TemplateResponse(
                        request,
                        "loans/get_loan.html",
                        {
                            "request": request,
                            "loans": loans,
                            "msg": msg,
                            "page": page,
                            "limit": limit,
                            "total_pages": total_pages
                        }
                    )
                else:
                    msg = {"detail":"Not enough copies to borrow","status":"failure"}
                    borrowers = Borrowers.Borrower.get_borrower()
                    books = Loans.Loan.get_unborrowed_book()
                    return templates.TemplateResponse(
                        request,
                        "loans/add_loan.html",
                        {"request":request,"borrowers":borrowers,"books":books,"loan_cart":loan_cart,"msg":msg}
                    )
    page = 1
    limit = 10
    offset = (page - 1) * limit

    loans = Loans.Loan.get_loan(limit, offset)
    total_loans = Loans.Loan.count_loans()
    total_pages = (total_loans + limit - 1) // limit

    return templates.TemplateResponse(
        request,
        "loans/get_loan.html",
        {
            "request": request,
            "loans": loans, 
            "msg": msg,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    )
#----------------------------------------------------------
@app.get("/return-loan/{id}")
def return_loan(request:Request,id:int):
    msg = Loans.Loan.return_loan(id)
    page = 1
    limit = 10
    offset = (page - 1) * limit

    loans = Loans.Loan.get_loan(limit, offset)
    total_loans = Loans.Loan.count_loans()
    total_pages = (total_loans + limit - 1) // limit

    return templates.TemplateResponse(
        request,
        "loans/get_loan.html",
        {
            "request": request,
            "loans": loans,
            "msg": msg,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    )

#-----------------------------------------------------------
@app.get("/update-loan-page/{id}")
def update_loan_page(request:Request,id:int):
    o_book,o_borrower,o_book_name,o_borrower_name,issued_books = Loans.Loan.get_detail_loan(id)
    books,borrowers = Loans.Loan.get_items_for_loan(id)
    return templates.TemplateResponse(  
        request,
        "loans/update_loan.html",
        {"request":request,"id":id,"o_book":o_book,"o_borrower":o_borrower,"o_book_name":o_book_name,"o_borrower_name":o_borrower_name,"borrowers":borrowers,"books":books,"issued_books":issued_books}
    )
@app.post("/update-loan")
def update_loan(request:Request,id:int=Form(...),book_id:int = Form(...),borrower_id:int = Form(...),issued_books:int=Form(...)):
    if issued_books is None or issued_books < 1:
        msg = {"detail": "Issued books must be at least 1", "status": "failure"}
    else:
        book_data = Loans.Loan.get_issued_books_loan(book_id)
        if isinstance(book_data, dict) and book_data.get("status") == "failure":
            msg = book_data
        else:
            total_books = book_data.get('total_books')
            current_total_issued = book_data.get('issued_books')
            old_loan_data = Loans.Loan.get_single_loan(id)
            if isinstance(old_loan_data, dict) and old_loan_data.get("status") == "failure":
                msg = old_loan_data
            else:
                old_loan = old_loan_data.get('issued_books', 0) if isinstance(old_loan_data, dict) else 0
                if total_books is None or current_total_issued is None:
                    msg = {"detail": "Unable to validate stock for this book", "status": "failure"}
                else:
                    new_total_issued = current_total_issued - old_loan + issued_books
                    if new_total_issued <= total_books:
                        msg = Loans.Loan.update_loan(id, book_id, borrower_id, issued_books)
                    else:
                        msg = {"detail": "Not enough copies to borrow", "status": "failure"}
    page = 1
    limit = 10
    offset = (page - 1) * limit

    loans = Loans.Loan.get_loan(limit, offset)
    total_loans = Loans.Loan.count_loans()
    total_pages = (total_loans + limit - 1) // limit

    return templates.TemplateResponse(
        request,
        "loans/get_loan.html",
        {
            "request": request,
            "loans": loans,
            "msg": msg,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    )
#---------------------------------------------------------------
@app.post("/get-loan-cart")
def get_loan_cart(request:Request,borrower_name:str = Form(...),book_name:str = Form(...),quantity:int=Form(...)):
    books = Loans.Loan.get_unborrowed_book()
    book_id = Books.Book.get_book_by_name(book_name)
    if book_id is None:
        msg = {"detail":"Book not found","status":"failure"}
    else:
        available = Loans.Loan.get_available_books(book_id)['remaining_quantity']
        loan_cart = Loans_cart.Loan_cart.get_loan_cart()
        current_quantity = sum(item['quantity'] for item in loan_cart if item['book_name'].lower() == book_name.lower())
        if current_quantity + quantity <= available:
            loan = Loans_cart.Loan_cart(Book_Name=book_name,Quantity=quantity)
            loan.add_loan_cart()
            loan_cart = Loans_cart.Loan_cart.get_loan_cart()
            return templates.TemplateResponse(
                request,
                "loans/add_loan.html",
                {"request":request,'books':books,'borrower_name':borrower_name,'loan_cart':loan_cart})
        msg = {"detail":f"Not enough copies to borrow. Available: {available - current_quantity}","status":"failure"}
    loan_cart = Loans_cart.Loan_cart.get_loan_cart()
    return templates.TemplateResponse(
        request,
        "loans/add_loan.html",
        {"request":request,'books':books,'borrower_name':borrower_name,'loan_cart':loan_cart,'msg':msg}
    )
@app.get('/delete-loan-cart/{id}')
def delete_loan_cart(request:Request,id:int,borrower_name:str = Query(None)):
    Loans_cart.Loan_cart.delete_loan_cart(id)
    books = Loans.Loan.get_unborrowed_book()
    loan_cart = Loans_cart.Loan_cart.get_loan_cart()
    return templates.TemplateResponse(
        request,
        "loans/add_loan.html",
        {"request":request,'books':books,'borrower_name':borrower_name,'loan_cart':loan_cart})