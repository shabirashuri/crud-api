from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
from utils.jwt_utils import decode_access_token
import models
from database import engine
from routes import  user_routes 
from routes import post_routes 
from routes import comment_routes , like_routes

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

# JWT Middleware
@app.middleware("http")
async def jwt_auth_middleware(request: Request, call_next):
    # Public routes that should skip authentication
    public_paths = ["/post/search","/user/login", "/user/register", "/docs", "/openapi.json"]

    # Allow public routes
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    # Check Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Authorization token missing"})

    token = auth_header.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

    # Store user info in request.state for later use in routes
    request.state.user = payload

    # Continue to the route
    return await call_next(request)

# Include routes
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(post_routes.router, prefix="/post", tags=["Post"]) 
app.include_router(comment_routes.router, prefix="/comments", tags=["omments"]) 
app.include_router(like_routes.router,prefix="/likes", tags=["Likes"]) 







