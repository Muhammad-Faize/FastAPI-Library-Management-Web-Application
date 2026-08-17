from pydantic import BaseModel
from datetime import datetime,timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext    
from fastapi import Request,Depends,HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM =  'HS256'
TOKEN_EXPIRE_MINUTE = 60

def create_access_token(username,role):
    expiry = datetime.utcnow() + timedelta(minutes = TOKEN_EXPIRE_MINUTE)
    payload ={
        "sub":username,
        "role":role,
        "exp":expiry,
    }
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token 

def current_user(request:Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401,detail="Not logged in ")
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        role = payload.get('role')
        return {'username':username,'role':role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
def require_role(allowed_roles:list):
    def role_checker(user:dict = Depends(current_user)):
        if user['role'] not in allowed_roles:
            raise HTTPException(status_code=403,detail="Not authorized for this action.")
        return user
    return role_checker

def optional_user(request:Request):
    token = request.cookies.get('access_token')
    if not token:
        return None
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        role = payload.get('role')
        return {"username":username,"role":role}
    except JWTError:
        return None

