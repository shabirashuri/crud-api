from fastapi import FastAPI
import models
from database import engine
from routes import  user_routes 
from routes import post_routes 

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

# Include routes
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(post_routes.router, prefix="/post", tags=["Post"]) 







