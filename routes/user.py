from fastapi import Request,Form,APIRouter,Depends
from fastapi.responses import RedirectResponse
import backend.Users as Users
from config import templates
import auth
from pydantic import EmailStr

router = APIRouter()

@router.get('/get-user')
def get_user(request:Request,user:dict = Depends(auth.require_role(['admin','user']))):
    users = Users.User.get_user()
    return templates.TemplateResponse(
        request,
        "users/get_user.html",
        {"request":request,"users":users}
    )
    
@router.get('/add-user-page')
def add_user_page(request:Request,user:dict = Depends(auth.require_role(['admin']))):
    return templates.TemplateResponse(
        request,
        "users/add_user.html",   
        {'request':request}
    )

@router.post('/add-user')
def add_user(request:Request,username:str = Form(...),email:str = Form(...),password:str = Form(...),user:dict = Depends(auth.require_role(['admin']))):
    user = Users.User(username=username,email=email,password=password)
    msg = user.register()
    users = Users.User.get_user()
    if msg['status'] == "success":
        return templates.TemplateResponse(
            request,
            "users/get_user.html",
            {'request':request,'msg':msg,'users':users}
        )
    else:
        return templates.TemplateResponse(
        request,
        "users/add_user.html",   
        {'request':request,'msg':msg}
        )
        

@router.get('/delete-user/{id}')
def delete_user(request:Request,id:int,user:dict = Depends(auth.require_role(['admin']))):
    msg = Users.User.delete_user(id)
    users = Users.User.get_user()
    return templates.TemplateResponse(
        request,
        "users/get_user.html",
        {"request":request,"users":users,"msg":msg}
    )

@router.get('/update-user-page/{id}')
def update_user_page(request:Request,id:int,user:dict = Depends(auth.require_role(['admin']))):
    data = Users.User.get_user_detail(id)
    return templates.TemplateResponse(
        request,
        "users/update_user.html",
        {'request':request,'id':id,'data':data}
    )

@router.post('/update-user')
def update_user(request:Request,id:int = Form(...),username:str=Form(...),email:EmailStr = Form(...),password:str = Form(default=''),user:dict = Depends(auth.require_role(['admin']))):
    msg = Users.User.update_user(id,username,email,password)
    users = Users.User.get_user()
    if msg['status'] == 'success':
        return templates.TemplateResponse(
            request,
            'users/get_user.html',
            {'request':request,'msg':msg,'users':users}
        )
    else:
        data = Users.User.get_user_detail(id)
        return templates.TemplateResponse(
            request,
            "users/update_user.html",
            {'request':request,'id':id,'data':data,'msg':msg}
        )

@router.get('/login-page')
def login_page(request:Request):
    return templates.TemplateResponse(
        request,
        "Authentication/login.html",
        {"request":request}
    )

@router.post('/login')
def login(request:Request,username:str = Form(...),password:str = Form(...)):   
    login_data = Users.User.login(username,password)
    if login_data['status'] == "success":
        token = auth.create_access_token(login_data['username'],login_data['role'])
        redirect = RedirectResponse(url='/',status_code=303)
        redirect.set_cookie(key="access_token",value=token,httponly=True)
        return redirect 
    else:
        return templates.TemplateResponse(
            request,
            "Authentication/login.html",
            {'request':request,'msg':login_data}
        )
@router.get('/logout')
def logout(request:Request):
    redirect = RedirectResponse(url='/login-page',status_code=303)
    redirect.delete_cookie('access_token')
    return redirect