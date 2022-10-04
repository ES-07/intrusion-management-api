from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from app.redis import init_redis_pool

app = FastAPI()
# incluir router mais tarde

@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis_pool()
    # criar repositório bd

@app.get("/hello")
def hello():
    return {"message": "Hello world. O projeto está feito meus caros"}

