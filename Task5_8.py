
# Import necessary modules from FastAPI
from fastapi import FastAPI, HTTPException
from typing import Optional

# Create an instance of the FastAPI class
app = FastAPI()

# Define a GET endpoint /convert_temp that takes 'temp' and 'unit' as query parameters
@app.get("/convert_temp")
async def convert_temp(temp: float, unit: Optional[str] = None):
    # If the unit is 'celsius', convert the temperature to Fahrenheit
    if unit == "celsius":
        converted_temp = (temp * 9/5) + 32
        unit = "fahrenheit"
    # If the unit is 'fahrenheit', convert the temperature to Celsius
    elif unit == "fahrenheit":
        converted_temp = (temp - 32) * 5/9
        unit = "celsius"
    # If the unit is not specified or invalid, raise an HTTP exception
    else:
        raise HTTPException(status_code=400, detail="Invalid or missing unit. Use 'celsius' or 'fahrenheit'.")

    # Return the converted temperature as a JSON response
    return {"converted_temp": round(converted_temp, 2), "unit": unit}

# Run the FastAPI app using Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
