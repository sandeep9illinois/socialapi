
from cgitb import reset
import time
from app import models, schemas, utils, oauth2
from app.database import engine, get_db

import psycopg2  
from psycopg2.extras import RealDictCursor
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter


router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

@router.get("/", response_model=List[schemas.Post])
#@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip:int =0, search:Optional[str] =""):
    # cursor.execute(""" SELECT * from posts""")
    # posts = cursor.fetchall()
    #print(limit, skip, search)
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #print(results)
    return posts
    #return results

#title  str
#content  str
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" insert into Posts (title, content, published) values (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(post.dict())
    print(current_user.email, current_user.id)
    #new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    '''
    def create_post(post: Post):
    print(post)
    print(post.dict())
    post_dict = post.dict()
    post_dict["id"] = randrange(0,10000000)
    my_post.append(post_dict)
    return {"Data ": post_dict}
    '''


@router.get("/{id}", response_model=schemas.Post)  #path parameter 
def get_single_post(id: int, db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user), limit: int = 10):
    # cursor.execute(""" SELECT * from posts where id = %s """, str(id))
    # posts = cursor.fetchone()
    print(limit)
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} not found")
    else:
        return posts

    '''post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} not found")
    return {"post_detail": post}'''



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
    #deleteing  post
    # cursor.execute(""" Delete from posts where id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    dl_post = deleted_post.first()
    if dl_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with passed id {id} not found")
    
    if dl_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised to perform requested action")
        
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    '''idx = find_index_post(id)
    if idx==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with passed id {id} not found")

    my_post.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)'''



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate , db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title = %s, content = %s where id = %s returning * """, (post.title, post.content, str(id), ))
    # updated_record = cursor.fetchone()
    # conn.commit()
    post_q = db.query(models.Post).filter(models.Post.id == id)
    updated_record = post_q.first()

    if updated_record == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with passed id {id} not found")
    
    if updated_record.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised to perform requested action")

    post_q.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_q.first()

    '''
    idx = find_index_post(id)
    print(idx, id)
    if idx==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with passed id {id} not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[idx] =  post_dict

    return {"messge": post_dict}'''