from fastapi import FastAPI
from contextlib import asynccontextmanager
from .Mongo_Connection import connect_to_mongo, close_mongo_connection
from .Features import user, notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await connect_to_mongo()
    print("Connected to MongoDB")

    yield  
    
    await close_mongo_connection()
    print("MongoDB connection closed")


app = FastAPI(
    title="Notes App",
    description="Backend for Notes App (MongoDB)",
    version="2.0",
    lifespan=lifespan,  
)



app.include_router(user.router)
app.include_router(notes.router)


@app.get("/")
def home():
    return {"message": "Notes API (MongoDB) is running!"}
