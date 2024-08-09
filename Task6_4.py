
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, condecimal

app = FastAPI()

# Define a Pydantic model for the input parameters
class OperationInput(BaseModel):
    x: condecimal(gt=-10**10, lt=10**10)  # Validate the input to be within a reasonable range
    y: condecimal(gt=-10**10, lt=10**10)
    operation: str

# Dependency to validate the input parameters
def get_operation_input(x: float, y: float, operation: str) -> OperationInput:
    if operation not in ["add", "subtract", "multiply", "divide"]:
        raise HTTPException(status_code=400, detail="Invalid operation. Choose from 'add', 'subtract', 'multiply', 'divide'.")
    return OperationInput(x=x, y=y, operation=operation)

@app.get("/calculate/")
async def calculate(input: OperationInput = Depends(get_operation_input)):
    x = input.x
    y = input.y
    operation = input.operation

    if operation == "add":
        result = x + y
    elif operation == "subtract":
        result = x - y
    elif operation == "multiply":
        result = x * y
    elif operation == "divide":
        if y == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        result = x / y
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    return {"result": result}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
