from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional
import secrets

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI app instance
app = FastAPI()

# User model for SQLAlchemy
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True, index=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic models for request and response data validation
class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    username: str
    api_key: str

# Dependency to get the current database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility function to create an API key
def generate_api_key():
    return secrets.token_hex(16)

# Utility function to validate API key
def get_user_by_api_key(db, api_key: str):
    return db.query(User).filter(User.api_key == api_key).first()

# User registration endpoint
@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    api_key = generate_api_key()
    new_user = User(username=user.username, api_key=api_key)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(username=new_user.username, api_key=new_user.api_key)

# Dependency to validate API key for protected endpoints
def api_key_auth(api_key: Optional[str] = None, db: SessionLocal = Depends(get_db)):
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="API key missing")
    user = get_user_by_api_key(db, api_key)
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")
    return user

# Protected endpoint that requires a valid API key
@app.get("/protected")
def read_protected_data(current_user: User = Depends(api_key_auth)):
    return {"message": f"Hello, {current_user.username}!"}

# To run the app, use: uvicorn main:app --reload
