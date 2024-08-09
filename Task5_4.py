
# Import necessary modules from FastAPI
from fastapi import FastAPI
from typing import Optional

# Create an instance of the FastAPI class
app = FastAPI()

# Define a GET endpoint /length that takes a query parameter 'text'
@app.get("/length")
async def get_length(text: Optional[str] = None):
    # If the 'text' query parameter is not provided, return an error message
    if text is None:
        return {"error": "Please provide a text query parameter"}
    # Calculate the length of the provided text
    length = len(text)
    # Return the length of the text as a JSON response
    return {"length": length}

# Run the FastAPI app using Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
