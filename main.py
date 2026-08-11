from fastapi import Form
from fastapi import FastAPI, Request,Query
from fastapi.staticfiles import StaticFiles
import Create_table 
from config import templates
 
from routes import author
from routes import borrower
from routes import book
from routes import loan


app = FastAPI() 
Create_table.create_table()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def menu_page(request: Request):
    return templates.TemplateResponse(
        request=request,    
        name="index.html",
        context={
            "request": request  
        })
        
app.include_router(author.router)
app.include_router(borrower.router)
app.include_router(book.router)
app.include_router(loan.router)
    