from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import Base, engine
from routers import auth, scholarship,application
from models.user import UserTable 
from models.scholarship import ScholarshipTable
from models.application import ApplicationTable
 
load_dotenv()
 
app = FastAPI()
 
Base.metadata.create_all(bind=engine)
 
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(scholarship.router, prefix="/scholarship", tags=["scholarship"])
app.include_router(application.router, prefix="/application", tags=["application"])