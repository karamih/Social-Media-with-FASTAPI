from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..databases import get_db
from .. import models, schemas, oauth2

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.Post])
def get_users(db: Session = Depends(get_db),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_user(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid id')

    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="you have to authorized to perform this action.")

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='post with this id unavailable')

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    new_post_query = db.query(models.Post).filter(models.Post.id == id)

    new_post = new_post_query.first()

    if new_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You have to authorized to perform this action.")

    if new_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='invalid id')
    new_post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return new_post
