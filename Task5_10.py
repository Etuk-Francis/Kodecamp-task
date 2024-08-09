
# Import necessary modules from FastAPI and random
from fastapi import FastAPI, Query
import random

# Create an instance of the FastAPI class
app = FastAPI()

# Define a GET endpoint /random that takes 'min' and 'max' as query parameters
@app.get("/random")
async def get_random(min: int = Query(..., description="Minimum value (inclusive)"),
                     max: int = Query(..., description="Maximum value (inclusive)")):
    # Check if min is greater than max
    if min > max:
        return {"error": "Minimum value cannot be greater than maximum value"}

    # Generate a random number between min and max (inclusive)
    random_number = random.randint(min, max)
    
    # Return the random number as a JSON response
    return {"random_number": random_number}

# Run the FastAPI app using Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
