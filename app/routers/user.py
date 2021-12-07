
import time
from app import models, schemas, utils
from app.database import engine, get_db

import psycopg2  
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter


router = APIRouter(
    prefix="/users",
    tags = ['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hash_pwd = utils.hash(user.password)
    user.password = hash_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)  #path parameter 
def get_single_user(id: int, db: Session = Depends(get_db)):
    userval = db.query(models.User).filter(models.User.id == id).first()
    if not userval:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with {id} not found")
    else:
        return userval