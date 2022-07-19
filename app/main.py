from fastapi import FastAPI
from app.routers import users

app: FastAPI = FastAPI()
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"Description": f"Please review the doc page: {app.openapi_url}"}
