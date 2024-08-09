
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from PIL import Image
import io

app = FastAPI()

# Dependency to validate image dimensions and format
def validate_image(file: UploadFile = File(...)) -> UploadFile:
    valid_formats = ["jpeg", "png", "jpg"]
    try:
        # Read the image file
        image = Image.open(file.file)
        # Validate the format
        if image.format.lower() not in valid_formats:
            raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are allowed.")
        # Validate the dimensions
        width, height = image.size
        if width > 1024 or height > 1024:
            raise HTTPException(status_code=400, detail="Image dimensions should not exceed 1024x1024 pixels.")
        # Reset the file pointer
        file.file.seek(0)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
    
    return file

@app.post("/upload-profile-picture/")
async def upload_profile_picture(file: UploadFile = Depends(validate_image)):
    # Simulate saving the image file or processing it
    # In a real application, you might save the file to a directory or cloud storage

    return {"filename": file.filename, "message": "Profile picture uploaded successfully"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
