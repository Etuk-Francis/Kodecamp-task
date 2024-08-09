
# Import necessary modules from FastAPI
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a GET endpoint /check_age/{age} that takes an age as a path parameter
@app.get("/check_age/{age}")
async def check_age(age: int):
    # Check if the provided age is 18 or older
    if age >= 18:
        return {"status": "Adult"}
    else:
        return {"status": "Not an adult"}

# Run the FastAPI app using Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
