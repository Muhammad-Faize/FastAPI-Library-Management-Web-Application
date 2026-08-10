from fastapi import Form
from fastapi import FastAPI, Request,Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import backend.Authors as Authors,backend.Books as Books,backend.Borrowers as Borrowers,backend.Loans as Loans,Create_table,backend.Loans_cart as Loans_cart,Connection
 
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
