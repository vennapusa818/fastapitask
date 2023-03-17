
# from sqlalchemy.orm import Session
#
# from . import crud, models, schemas
# from .database import SessionLocal, engine
#
#
# from datetime import datetime, timedelta
# from typing import Optional
#
# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
#
# from passlib.context import CryptContext
#
#
# models.Base.metadata.create_all(bind=engine)
#
# app = FastAPI()
#
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, pwd_context.hash(hashed_password))
#
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# def get_user(db: Session, username: str):
#     return db.query(models.User).filter(models.User.username == username).first()
#
#
# def authenticate_user(db: Session, username: str, password: str):
#     user = get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
#
#
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> schemas.User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# def get_current_active_user(current_user: schemas.User = Depends(get_current_user)) -> schemas.User:
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# @app.post("/token", response_model=schemas.Token)
# def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @app.get("/users/me/", response_model=schemas.User)
# def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
#     return current_user
#
#
# #main api's
# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)
#
#
# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
#     if current_user:
#         users = crud.get_users(db, skip=skip, limit=limit)
#         return users
#
#
# @app.get("/users/{user_email}", response_model=schemas.User)
# def read_user(email: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
#     if current_user:
#         db_user = crud.get_user_by_email(db, email=email.lower())
#         if db_user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return db_user
#
# #UserProfile
#
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
#
#
# @app.delete("/items/{item_id}")
# def user_profile_retrive(item_id:int, db: Session = Depends(get_db)):
#     crud.drop_item(db, item_id)
#     return None
#
#
# @app.put("/items/{item_id}", response_model=schemas.Item)
# def user_profile_update_and_delete(item_id: int, action:str, data: schemas.ItemUpdate,  db: Session = Depends(get_db)):
#     if action == "Add":
#         item = crud.update_item(db, item_id, data)
#         if item is None:
#             raise HTTPException(status_code=404)
#         return item
#     if action == "Remove":
#         crud.drop_item(db, item_id)
#         return None
#
#
# @app.post("/users/{user_id}/ads/", response_model=schemas.Ad)
# def create_ad_for_user(
#     user_id: int, ad: schemas.AdCreate, db: Session = Depends(get_db)):
#     return crud.create_user_ad(db=db, ad=ad, user_id=user_id)
#
#
# @app.get("/ads/", response_model=list[schemas.Ad])
# def read_ads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     ads = crud.get_ads(db, skip=skip, limit=limit)
#     return ads
#
#
# # @app.delete("/ads/{ad_id}")
# # def ad_action_drop(ad_id:int, db: Session = Depends(get_db)):
# #     crud.drop_ad(db, ad_id)
# #     return None
#
#
# @app.put("/ads/{ad_id}", response_model=schemas.Ad)
# def ad_profile_update_and_delete(ad_id: int, action:str, data: schemas.AdUpdate,  db: Session = Depends(get_db)):
#     if action == "Add":
#         ad = crud.update_ad(db, ad_id, data)
#         if ad is None:
#             raise HTTPException(status_code=404)
#         return ad
#     if action == "Remove":
#         crud.drop_ad(db, ad_id)
#         return None
#

# FAKE DB

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "rajesh": {
        "username": "rajesh",
        "full_name": "rajesh",
        "email": "rajesh@gmail.com",
        "hashed_password": "$2b$12$G3vPtttDB3bfgz5X8o0Dc.37C6V/D9R4jYjncaao3IN1mnMRUwTd2",  # rajesh@123
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user







