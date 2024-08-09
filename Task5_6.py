
# Import necessary modules from FastAPI
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a GET endpoint /square/{number} that takes a number as a path parameter
@app.get("/square/{number}")
async def get_square(number: int):
    # Calculate the square of the provided number
    square = number ** 2
    # Return the square of the number as a JSON response
    return {"square": square}

# Run the FastAPI app using Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
