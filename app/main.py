# main.py
from fastapi import FastAPI
from app.routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI CRUD Application",
    description="A simple API to demonstrate FastAPI with SQLAlchemy.",
    version="1.0.0",
)

origins = [
    "https://localhost",
    "http://localhost",
    "http://localhost:8000",
    "https://www.google.com",
    "https://www.youtube.com",
]

# CORS
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow credentials
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include Routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI CRUD Application"}
