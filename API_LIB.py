from fastapi import FastAPI

app = FastAPI()

 # Function decorator (type of http request, route or url or endpoint)
 # Function itself
 # Function return statement

@app.get('/v1/forecast')
def root():
    return{"message": "our first appi endpoint"}