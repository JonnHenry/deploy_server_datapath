from fastapi import FastAPI
from routes import router_

app = FastAPI()
app.include_router(router_)
