from fastapi import FastAPI
import logging

from .database import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware
from .routers import packs, users, picks, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

logging.basicConfig(level=logging.INFO)


app.include_router(packs.router)
app.include_router(picks.router)
app.include_router(users.router)
app.include_router(auth.router)

print('hello world')



@app.get("/")
def read_root():
    return {"Hello": "World"}

    
