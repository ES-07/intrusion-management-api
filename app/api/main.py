from fastapi import FastAPI, HTTPException
from starlette.responses import Response

app = FastAPI()
# incluir router mais tarde

@app.get("/hello")
def hello():
    return {"message": "Hello world. O projeto está feito meus caros"}

