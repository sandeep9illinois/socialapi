from dbm.dumb import _Database
from enum import auto
from importlib.resources import contents
from operator import mod, pos
import secrets
from statistics import mode
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from app.routers import post, user , auth, vote
from app.config import settings

#from random import randrange

#import psycopg2  
#from psycopg2.extras import RealDictCursor
#from sqlalchemy.orm import Session

#import time
from app import models, schemas, utils
from app.database import engine, get_db

from fastapi.middleware.cors import CORSMiddleware


print(settings.database_username)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins =["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# my_post =[{"title":"title value1", "content":"content of title1", "id": 1}, 
# {"title":"fav pizza", "content":"i like it", "id": 2}]


# def find_post(id):
#     for p in my_post:
#         if p["id"]==id:
#             return p


# def find_index_post(id):
#     for i,p in enumerate(my_post):
#         if p["id"] == id:
#             return i

#path operations

# @app.get("/sqlalchamy")
# def test_posts(db: Session = Depends(get_db)):

#     posts = db.query(models.Post).filter_by(id=2)
#     print(posts)
#     return {"data":"posts"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Welcome onboard"}


# @app.get("/posts", response_model=List[schemas.Post])
# def get_post(db: Session = Depends(get_db)):
#     # cursor.execute(""" SELECT * from posts""")
#     # posts = cursor.fetchall()
#     posts = db.query(models.Post).all()
#     return posts

# #title  str
# #content  str
# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
#     # cursor.execute(""" insert into Posts (title, content, published) values (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     # new_post = cursor.fetchone()
#     # conn.commit()
#     print(post.dict())
#     #new_post = models.Post(title = post.title, content = post.content, published = post.published)
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post
#     '''
#     def create_post(post: Post):
#     print(post)
#     print(post.dict())
#     post_dict = post.dict()
#     post_dict["id"] = randrange(0,10000000)
#     my_post.append(post_dict)
#     return {"Data ": post_dict}
#     '''


# @app.get("/posts/{id}", response_model=schemas.Post)  #path parameter 
# def get_single_post(id: int, db: Session = Depends(get_db)):
#     # cursor.execute(""" SELECT * from posts where id = %s """, str(id))
#     # posts = cursor.fetchone()
#     posts = db.query(models.Post).filter(models.Post.id == id).first()
#     if not posts:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with {id} not found")
#     else:
#         return posts

#     '''post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with {id} not found")
#     return {"post_detail": post}'''



# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db)):
#     #deleteing  post
#     # cursor.execute(""" Delete from posts where id = %s returning *""",(str(id),))
#     # deleted_post = cursor.fetchone()
#     # conn.commit()
#     deleted_post = db.query(models.Post).filter(models.Post.id == id)

#     if deleted_post.first()==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with passed id {id} not found")
    
#     deleted_post.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)

#     '''idx = find_index_post(id)
#     if idx==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with passed id {id} not found")

#     my_post.pop(idx)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)'''



# @app.put("/posts/{id}", response_model=schemas.Post)
# def update_post(id: int, post: schemas.PostCreate , db: Session = Depends(get_db)):
#     # cursor.execute("""update posts set title = %s, content = %s where id = %s returning * """, (post.title, post.content, str(id), ))
#     # updated_record = cursor.fetchone()
#     # conn.commit()
#     post_q = db.query(models.Post).filter(models.Post.id == id)
#     updated_record = post_q.first()

#     if updated_record == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with passed id {id} not found")
#     post_q.update(post.dict(), synchronize_session=False)
#     db.commit()
#     return post_q.first()

#     '''
#     idx = find_index_post(id)
#     print(idx, id)
#     if idx==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with passed id {id} not found")
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_post[idx] =  post_dict

#     return {"messge": post_dict}'''

# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     # hash the password - user.password
#     hash_pwd = utils.hash(user.password)
#     user.password = hash_pwd

#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.get("/users/{id}", response_model=schemas.UserOut)  #path parameter 
# def get_single_user(id: int, db: Session = Depends(get_db)):
#     userval = db.query(models.User).filter(models.User.id == id).first()
#     if not userval:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"user with {id} not found")
#     else:
#         return userval
