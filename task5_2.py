
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/add/{a}/{b}")
async def add(a: float, b: float):
    return {"result": a + b}

@app.get("/subtract/{a}/{b}")
async def subtract(a: float, b: float):
    return {"result": a - b}

@app.get("/multiply/{a}/{b}")
async def multiply(a: float, b: float):
    return {"result": a * b}

@app.get("/divide/{a}/{b}")
async def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    return {"result": a / b}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
