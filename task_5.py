
from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

@app.get("/validate_number/{number}")
async def validate_number(number: int, min: Optional[int] = None, max: Optional[int] = None):
    if min is not None and number < min:
        return False
    if max is not None and number > max:
        return False
    return True

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
