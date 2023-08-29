from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import posts, users, auth, votes


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "Hello"}


app.include_router(router=posts.router)
app.include_router(router=users.router)
app.include_router(router=auth.router)
app.include_router(router=votes.router)