from fastapi import Form,HTTPException
from fastapi import FastAPI, Request,Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import Create_table 
from config import templates
 
from routes import author
from routes import borrower
from routes import book
from routes import loan
from routes import user
import auth


app = FastAPI() 

Create_table.create_table()

app.mount("/static", StaticFiles(directory="static"), name="static")
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

@app.exception_handler(HTTPException)
def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return RedirectResponse(url="/login-page", status_code=303)
    elif exc.status_code == 403:
        return templates.TemplateResponse(
            request,
            "errors/403.html",
            {"request": request, "detail": exc.detail},
            status_code=403
        )
    return templates.TemplateResponse(
        request,
        "errors/403.html",
        {"request": request, "detail": exc.detail},
        status_code=exc.status_code
    )
    
@app.get("/")
def menu_page(request: Request):
    user = auth.optional_user(request)
    if not user:
        return RedirectResponse(url="/login-page", status_code=303)
    return templates.TemplateResponse(
        request=request,    
        name="index.html",
        context={"request": request, "user": user}
    )
        
app.include_router(author.router)
app.include_router(borrower.router)
app.include_router(book.router)
app.include_router(loan.router)
app.include_router(user.router)