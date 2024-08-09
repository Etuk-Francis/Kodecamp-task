
# Import necessary modules from FastAPI and Pydantic
from fastapi import FastAPI
from pydantic import BaseModel

# Create an instance of the FastAPI class
app = FastAPI()

# Define a Pydantic model for the request body
class InterestCalculationRequest(BaseModel):
    principal: float
    rate: float
    time: float

# Define a POST endpoint /interest that takes principal, rate, and time in the request body
@app.post("/interest")
async def calculate_interest(interest_request: InterestCalculationRequest):
    # Calculate simple interest using the formula: SI = (P * R * T) / 100
    simple_interest = (interest_request.principal * interest_request.rate * interest_request.time) / 100
    # Return the calculated simple interest as a JSON response
    return {"simple_interest": round(simple_interest, 2)}

# Run the FastAPI app using Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
