from fastapi import APIRouter, Request, Form,Depends
import auth
import backend.Borrowers as Borrowers
from config import templates

router = APIRouter()

@router.get("/get-borrower")
def get_borrower(request:Request,user:dict = Depends(auth.require_role(['admin',"user"]))):
    borrowers= Borrowers.Borrower.get_borrower()
    return templates.TemplateResponse(
        request,
        "borrowers/get_borrower.html",
        {"request":request,
        "borrowers":borrowers}
    )
#-----------------------------------------------
@router.get("/add-borrower-page")
def add_borrower_page(request:Request,user:dict = Depends(auth.require_role(['admin']))):
    return templates.TemplateResponse(
        request,
        "borrowers/add_borrower.html",
        {"request":request}
    )

@router.post("/add-borrower")
def add_borrower(request:Request,name:str = Form(...),user:dict = Depends(auth.require_role(['admin']))):
    borrower = Borrowers.Borrower(name = name)
    msg = borrower.add_borrower()
    borrowers = Borrowers.Borrower.get_borrower()
    return templates.TemplateResponse(
        request,
        "borrowers/get_borrower.html",
        {"request":request,"borrowers":borrowers,"msg":msg}
    ) 

#------------------------------------------------  
@router.get("/delete-borrower/{id}")
def delete_borrower(request:Request,id:int,user:dict = Depends(auth.require_role(['admin']))):
    msg = Borrowers.Borrower.delete_borrower(id)
    borrowers = Borrowers.Borrower.get_borrower()
    return templates.TemplateResponse(
        request,
        "borrowers/get_borrower.html",
        {"request":request,"borrowers":borrowers,"msg":msg}
    ) 
#------------------------------------------------
@router.get("/update-borrower-page/{id}")
def update_borrower_page(request:Request,id:int,user:dict = Depends(auth.require_role(['admin']))):
    name = Borrowers.Borrower.get_borrower_by_id(id)
    return templates.TemplateResponse(
        request,
        "borrowers/update_borrower.html",
        {"request":request,"id":id,"name":name}
    )
    
@router.post("/update-borrower")
def update_borrower(request:Request,id:int = Form(...),name:str = Form(...),user:dict = Depends(auth.require_role(['admin']))):
    msg = Borrowers.Borrower.update_borrower(id,name)
    borrowers = Borrowers.Borrower.get_borrower()
    return templates.TemplateResponse(
        request,
        "borrowers/get_borrower.html",
        {"request":request,"borrowers":borrowers,"msg":msg}
    ) 
#-------------------------------------------------- 
@router.get("/get-borrower-details/{id}")
def get_borrower_detail(request:Request,id:int,user:dict = Depends(auth.require_role(['admin',"user"]))):
    borrower_books,borrower = Borrowers.Borrower.get_borrower_details(id)
    return templates.TemplateResponse(
        request,
        'borrowers/get_borrower_details.html',
        {'request':request,'id':id,'borrower_books':borrower_books,'borrower':borrower}
    )
#-------------------------------------------------------------
@router.get('/get-borrower-search')
def get_borrower_search(request: Request, search: str,user:dict = Depends(auth.require_role(['admin',"user"]))):  
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