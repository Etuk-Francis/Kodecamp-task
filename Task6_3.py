
from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel, EmailStr, constr
from typing import Optional

app = FastAPI()

# Dependency to validate resume file
def validate_resume(file: UploadFile = File(...)) -> UploadFile:
    valid_formats = ["pdf", "doc", "docx"]
    if file.filename.split(".")[-1].lower() not in valid_formats:
        raise HTTPException(status_code=400, detail="Invalid file format. Only PDF, DOC, and DOCX are allowed.")
    return file

# Pydantic model for text fields
class JobApplicationForm(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    cover_letter: Optional[str] = None

@app.post("/submit-application/")
async def submit_application(
    name: str = Form(...),
    email: str = Form(...),
    cover_letter: Optional[str] = Form(None),
    resume: UploadFile = Depends(validate_resume)
):
    # Validate required fields
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    # Simulate saving the data or processing the form
    # In a real application, you might save the data to a database or send an email
    
    return {
        "message": "Application submitted successfully",
        "data": {
            "name": name,
            "email": email,
            "cover_letter": cover_letter,
            "resume_filename": resume.filename
        }
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
