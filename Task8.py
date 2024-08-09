
# Import necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Create a FastAPI instance
app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./portfolio.db"  # SQLite database file
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Project model
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)

# Define the BlogPost model
class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)

# Define the ContactInfo model
class ContactInfo(Base):
    __tablename__ = "contact_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    message = Column(Text)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic models for request and response
class ProjectCreate(BaseModel):
    title: str
    description: str

class BlogPostCreate(BaseModel):
    title: str
    content: str

class ContactCreate(BaseModel):
    name: str
    email: str
    message: str

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Project endpoints
@app.post("/projects/", response_model=ProjectCreate)
def create_project(project: ProjectCreate, db: Session = next(get_db())):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects/", response_model=list[ProjectCreate])
def read_projects(skip: int = 0, limit: int = 10, db: Session = next(get_db())):
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects

@app.get("/projects/{project_id}", response_model=ProjectCreate)
def read_project(project_id: int, db: Session = next(get_db())):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=ProjectCreate)
def update_project(project_id: int, project: ProjectCreate, db: Session = next(get_db())):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project.dict().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = next(get_db())):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return {"detail": "Project deleted"}

# Blog post endpoints
@app.post("/blog_posts/", response_model=BlogPostCreate)
def create_blog_post(blog_post: BlogPostCreate, db: Session = next(get_db())):
    db_blog_post = BlogPost(**blog_post.dict())
    db.add(db_blog_post)
    db.commit()
    db.refresh(db_blog_post)
    return db_blog_post

@app.get("/blog_posts/", response_model=list[BlogPostCreate])
def read_blog_posts(skip: int = 0, limit: int = 10, db: Session = next(get_db())):
    blog_posts = db.query(BlogPost).offset(skip).limit(limit).all()
    return blog_posts

@app.get("/blog_posts/{blog_post_id}", response_model=BlogPostCreate)
def read_blog_post(blog_post_id: int, db: Session = next(get_db())):
    blog_post = db.query(BlogPost).filter(BlogPost.id == blog_post_id).first()
    if blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog_post

@app.put("/blog_posts/{blog_post_id}", response_model=BlogPostCreate)
def update_blog_post(blog_post_id: int, blog_post: BlogPostCreate, db: Session = next(get_db())):
    db_blog_post = db.query(BlogPost).filter(BlogPost.id == blog_post_id).first()
    if db_blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    for key, value in blog_post.dict().items():
        setattr(db_blog_post, key, value)
    db.commit()
    db.refresh(db_blog_post)
    return db_blog_post

@app.delete("/blog_posts/{blog_post_id}")
def delete_blog_post(blog_post_id: int, db: Session = next(get_db())):
    db_blog_post = db.query(BlogPost).filter(BlogPost.id == blog_post_id).first()
    if db_blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    db.delete(db_blog_post)
    db.commit()
    return {"detail": "Blog post deleted"}

# Contact information endpoints
@app.post("/contact_info/", response_model=ContactCreate)
def create_contact(contact: ContactCreate, db: Session = next(get_db())):
    db_contact = ContactInfo(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contact_info/", response_model=list[ContactCreate])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = next(get_db())):
    contacts = db.query(ContactInfo).offset(skip).limit(limit).all()
    return contacts

@app.delete("/contact_info/{contact_id}")
def delete_contact(contact_id: int, db: Session = next(get_db())):
    db_contact = db.query(ContactInfo).filter(ContactInfo.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"detail": "Contact deleted"}