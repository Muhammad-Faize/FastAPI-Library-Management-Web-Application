from fastapi import APIRouter, Request, Form

import backend.Authors as Authors
from config import templates

router = APIRouter()

@router.get('/get-author')
def get_author_page(request:Request):
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        'authors/get_author.html',
        {"request":request,"authors":authors}
    )
#---------------------------------------------
@router.get('/add-author-page')
def add_author_page(request:Request):
    return templates.TemplateResponse(
        request,    
        'authors/add_author.html'
    )
    
@router.post('/add-author')
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
@router.get('/delete-author/{id}')
def delete_author(request:Request,id:int):
    msg = Authors.Author.delete_author(id)
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        "authors/get_author.html",
        {"request":request,"authors":authors,"msg":msg}
    )
#---------------------------------------------
@router.get('/update-author-page/{id}')
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
@router.post('/update-author')
def update_author(request:Request,id:int = Form(...),name:str = Form(...)):
    msg = Authors.Author.update_author(id,name)
    authors = Authors.Author.get_auhtor()
    return templates.TemplateResponse(
        request,
        "authors/get_author.html",
        {"request":request,"authors":authors,"msg":msg}
    )    