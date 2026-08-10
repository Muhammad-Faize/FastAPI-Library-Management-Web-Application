from fastapi import APIRouter, Request, Form

import backend.Authors as Authors ,backend.Books as Books
from config import templates

router = APIRouter()

@router.get("/get-book")
def get_books(request:Request):
    books = Books.Book.get_book()
    return templates.TemplateResponse(
        request,
        "books/get_book.html",
        {"request":request,"books":books}
    )
#--------------------------------------------------
@router.get("/add-book-page")
def add_book_page(request:Request):
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        "books/add_book.html",
        {"request":request,"books":authors,"name":"","quantity":"","search":""}
    )
@router.post("/add-book")
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
@router.get("/delete-book/{id}")
def delete_book(request:Request,id:int):
    msg = Books.Book.delete_book(id)
    books = Books.Book.get_book()
    return templates.TemplateResponse(
        request,
        "books/get_book.html",
        {"request":request,"books":books,"msg":msg}
    ) 
#----------------------------------------------------
@router.get("/update-book-page/{id}")
def update_book_page(request:Request,id:int):
    name,quantity = Books.Book.get_book_by_id(id)
    return templates.TemplateResponse(
        request,
        "books/update_book.html",
        {"request":request,"id":id,"name":name,"quantity":quantity}
    )
@router.post("/update-book")
def update_book(request:Request,id:int = Form(...),name:str = Form(...),quantity:int=Form(...)):
    msg = Books.Book.update_book(id,name,quantity)
    books = Books.Book.get_book()
    return templates.TemplateResponse(
        request,
        "books/get_book.html",
        {"request":request,"books":books,"msg":msg}
    ) 
#-------------------------------------------------------------
@router.get('/get-book-search')
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
@router.post('/search-author')
def search_author(request:Request,search:str=Form(...),name:str=Form(default=""),quantity:int=Form(default=0)):
    results = Authors.Author.search_author(search)
    return templates.TemplateResponse(
        request,
        "books/add_book.html",
        {"request":request,"results":results,'search':search,'name':name,'quantity':quantity}
    )
@router.get('/get-issued-detail/{id}')
def get_issued_detail(request:Request,id:int):
    data = Books.Book.get_issued_detail(id)
    return templates.TemplateResponse(
        request,
        "books/get_issued_detail.html",
        {"request":request,"data":data}
    )