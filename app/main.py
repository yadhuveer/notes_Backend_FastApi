from fastapi import FastAPI
from . import SQL_Connection
from .SQL_Connection import engine
from .Features import user, notes;

SQL_Connection.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notes App",
    description="Backend for Notes App",
    version="1.0"
)


app.include_router(user.router)
app.include_router(notes.router)

@app.get("/")
def home():
    return {"message": "Notes API is running!"}
