
# Import necessary modules from FastAPI and Pydantic
from fastapi import FastAPI
from pydantic import BaseModel

# Create an instance of the FastAPI class
app = FastAPI()

# Define a Pydantic model for the request body
class BMICalculationRequest(BaseModel):
    weight: float
    height: float

# Define a POST endpoint /bmi that takes weight and height in the request body
@app.post("/bmi")
async def calculate_bmi(bmi_request: BMICalculationRequest):
    # Calculate BMI using the formula: BMI = weight (kg) / (height (m) ^ 2)
    bmi = bmi_request.weight / (bmi_request.height ** 2)
    # Return the calculated BMI as a JSON response
    return {"bmi": round(bmi, 2)}

# Run the FastAPI app using Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
