from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from ..databases import get_db
from ..oauth2 import get_current_user
from .. import schemas, models


router = APIRouter(prefix="/vote", tags=["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Could not find post with this id.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)

    if vote.dir == 1:
        if vote_query.first() is None:
            new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            return {"message": "liked successfully."}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="You've already liked this post.")
    else:
        if vote_query.first():
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "unliked successfully."}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="You've not alrady liked this post.")