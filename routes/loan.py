from fastapi import APIRouter, Request, Form
from fastapi import FastAPI, Request,Query,Depends
import backend.Loans as Loans, backend.Loans_cart as Loans_cart,backend.Borrowers as Borrowers,backend.Books as Books ,Connection
from config import templates
import auth

router = APIRouter()

@router.get("/get-loan")
def get_loans(request: Request, page: int = 1, limit: int = 10,user:dict = Depends(auth.require_role(['admin',"user"]))):

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
@router.get("/add-loan-page")
def add_loan_page(request:Request,user:dict = Depends(auth.require_role(['admin']))):
    borrowers = Borrowers.Borrower.get_borrower()
    books = Loans.Loan.get_unborrowed_book()
    return templates.TemplateResponse(
        request,
        "loans/add_loan.html",
        {"request":request,"borrowers":borrowers,"books":books}
    )
@router.post("/add-loan")
def add_loan(request: Request,borrower_name: str = Form(...),user:dict = Depends(auth.require_role(['admin']))):
    borrower_id = Borrowers.Borrower.get_borrower_by_name(borrower_name)
    loan_cart = Loans_cart.Loan_cart.get_loan_cart()
    if borrower_id is None:
        msg = {
            "detail": "Borrower does not exist",
            "status": "failure"
        }

        borrowers = Borrowers.Borrower.get_borrower()
        books = Loans.Loan.get_unborrowed_book()

        return templates.TemplateResponse(
            request,
            "loans/add_loan.html",
            {
                "request": request,
                "borrowers": borrowers,
                "books": books,
                "msg": msg
            }
        )

    for cart_item in loan_cart:

        book_name = cart_item["book_name"]
        quantity = cart_item["quantity"]

        book_id = Books.Book.get_book_by_name(book_name)

        if book_id is None:
            msg = {
                "detail": f"Book '{book_name}' does not exist",
                "status": "failure"
            }

            borrowers = Borrowers.Borrower.get_borrower()
            books = Loans.Loan.get_unborrowed_book()

            return templates.TemplateResponse(
                request,
                "loans/add_loan.html",
                {
                    "request": request,
                    "borrowers": borrowers,
                    "books": books,
                    "loan_cart": loan_cart,
                    "msg": msg
                }
            )

        available_data = Loans.Loan.get_available_books(book_id)

        available = available_data["remaining_quantity"]

        if available < quantity:
            msg = {
                "detail": (
                    f"Not enough copies of '{book_name}' to borrow. "
                    f"Available: {available}"
                ),
                "status": "failure"
            }

            borrowers = Borrowers.Borrower.get_borrower()
            books = Loans.Loan.get_unborrowed_book()

            return templates.TemplateResponse(
                request,
                "loans/add_loan.html",
                {
                    "request": request,
                    "borrowers": borrowers,
                    "books": books,
                    "loan_cart": loan_cart,
                    "msg": msg
                }
            )
        loan = Loans.Loan(
            borrower_id=borrower_id,
            book_id=book_id,
            issued_books=quantity
        )
        msg = loan.add_loan()
        if isinstance(msg, dict) and msg.get("status") == "failure":
            borrowers = Borrowers.Borrower.get_borrower()
            books = Loans.Loan.get_unborrowed_book()

            return templates.TemplateResponse(
                request,
                "loans/add_loan.html",
                {
                    "request": request,
                    "borrowers": borrowers,
                    "books": books,
                    "loan_cart": loan_cart,
                    "msg": msg
                }
            )
    con, cur = Connection.connection()
    cur.execute("TRUNCATE TABLE Loans_cart")
    con.commit()
    cur.close()
    Connection.release_connection(con)

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
@router.get("/return-loan/{id}")
def return_loan(request:Request,id:int,user:dict = Depends(auth.require_role(['admin']))):
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
@router.get("/update-loan-page/{id}")
def update_loan_page(request:Request,id:int,user:dict = Depends(auth.require_role(['admin']))):
    o_book,o_borrower,o_book_name,o_borrower_name,issued_books = Loans.Loan.get_detail_loan(id)
    books,borrowers = Loans.Loan.get_items_for_loan(id)
    return templates.TemplateResponse(  
        request,
        "loans/update_loan.html",
        {"request":request,"id":id,"o_book":o_book,"o_borrower":o_borrower,"o_book_name":o_book_name,"o_borrower_name":o_borrower_name,"borrowers":borrowers,"books":books,"issued_books":issued_books}
    )
@router.post("/update-loan")
def update_loan(request: Request,id: int = Form(...),book_id: int = Form(...),borrower_id: int = Form(...),issued_books: int = Form(...),user:dict = Depends(auth.require_role(['admin']))):
    msg = None
    if issued_books < 1:
        msg = {
            "detail": "Issued books must be at least 1",
            "status": "failure"
        }
    else:
        old_loan_data = Loans.Loan.get_single_loan(id)
        if (isinstance(old_loan_data, dict) and old_loan_data.get("status") == "failure"):
            msg = old_loan_data
        else:
            old_book_id = old_loan_data.get("book_id")
            old_issued_books = old_loan_data.get("issued_books", 0)
            book_data = Loans.Loan.get_issued_books_loan(book_id)

            if ( isinstance(book_data, dict)and book_data.get("status") == "failure"):
                msg = book_data

            else:
                total_books = book_data.get("total_books")
                current_total_issued = book_data.get("issued_books")

                if total_books is None or current_total_issued is None:
                    msg = {"detail": "Unable to validate stock for this book","status": "failure"}

                else:
                    if old_book_id == book_id:
                        # Return the old loan's books first
                        available_books = total_books - current_total_issued + old_issued_books
                    else:
                        # Old loan belongs to another book
                        available_books = total_books - current_total_issued

                    if issued_books <= available_books:
                        msg = Loans.Loan.update_loan(id, book_id,borrower_id,issued_books)
                    else:
                        msg = {"detail": "Not enough copies to borrow","status": "failure"}

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
@router.post("/get-loan-cart")
def get_loan_cart(request:Request,borrower_name:str = Form(...),book_name:str = Form(...),quantity:int=Form(...),user:dict = Depends(auth.require_role(['admin']))):
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
@router.get('/delete-loan-cart/{id}')
def delete_loan_cart(request:Request,id:int,borrower_name:str = Query(None),user:dict = Depends(auth.require_role(['admin']))):
    borrowers = Borrowers.Borrower.get_borrower()
    Loans_cart.Loan_cart.delete_loan_cart(id)
    books = Loans.Loan.get_unborrowed_book()
    loan_cart = Loans_cart.Loan_cart.get_loan_cart()
    return templates.TemplateResponse(
        request,
        "loans/add_loan.html",
        {"request":request,'books':books,'borrower_name':borrower_name,"borrowers":borrowers,'loan_cart':loan_cart})