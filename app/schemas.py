from pydantic import BaseModel, EmailStr


class PostCreate(BaseModel):
    title: str
    content: str
    is_published: bool = True


class UserOut(BaseModel):
    id: int
    email: EmailStr


class Post(PostCreate):
    is_published: bool
    id: int
    owner: UserOut

    class config:
        orm_mode = True


class PostOut(PostCreate):
    post: Post
    vote: int

    class config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr

    class config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int


class Vote(BaseModel):
    post_id: int
    dir: int