from fastapi import FastAPI

from app.routers import auth, games, users

app: FastAPI = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(games.router)


@app.get("/")
def read_root():
    return {"Description": f"Please review the doc page: {app.openapi_url}"}
