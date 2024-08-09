
from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel, EmailStr, constr
from typing import Optional

app = FastAPI()

# Define a Pydantic model for the contact form data
class ContactForm(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    message: constr(min_length=1)

@app.post("/submit-contact-form/")
async def submit_contact_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Validate required fields
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    # Simulate saving the data or processing the form
    # In a real application, you might save the data to a database or send an email
    
    return {"message": "Form submitted successfully", "data": {"name": name, "email": email, "message": message}}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
