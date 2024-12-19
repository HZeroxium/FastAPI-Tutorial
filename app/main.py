# main.py
from fastapi import FastAPI
from app.routers import post, user, auth

app = FastAPI(
    title="FastAPI CRUD Application",
    description="A simple API to demonstrate FastAPI with SQLAlchemy.",
    version="1.0.0",
)

# Include Routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI CRUD Application"}
