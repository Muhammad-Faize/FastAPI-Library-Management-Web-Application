from fastapi import APIRouter, Request, Form,Depends
import auth
import backend.Authors as Authors
from config import templates

router = APIRouter()

@router.get('/get-author')
def get_author_page(request:Request,user:dict = Depends(auth.require_role(['admin',"user"]))):
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        'authors/get_author.html',
        {"request":request,"authors":authors}
    )
#---------------------------------------------
@router.get('/add-author-page')
def add_author_page(request:Request,user:dict = Depends(auth.require_role(['admin']))):
    return templates.TemplateResponse(
        request,    
        'authors/add_author.html'
    )
    
@router.post('/add-author')
def add_author(request:Request,name:str = Form(...),user:dict = Depends(auth.require_role(['admin']))):
    author = Authors.Author(name = name)
    msg = author.add_author()
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        "authors/get_author.html",
        {"request":request,"authors":authors,"msg":msg}
    )
#----------------------------------------------
@router.get('/delete-author/{id}')
def delete_author(request:Request,id:int,user:dict = Depends(auth.require_role(['admin']))):
    msg = Authors.Author.delete_author(id)
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        "authors/get_author.html",
        {"request":request,"authors":authors,"msg":msg}
    )
#---------------------------------------------
@router.get('/update-author-page/{id}')
def update_author_page(request:Request,id:int,user:dict = Depends(auth.require_role(['admin']))):
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
@router.post('/update-author')
def update_author(request:Request,id:int = Form(...),name:str = Form(...),user:dict = Depends(auth.require_role(['admin']))):
    msg = Authors.Author.update_author(id,name)
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        "authors/get_author.html",
        {"request":request,"authors":authors,"msg":msg}
    )    