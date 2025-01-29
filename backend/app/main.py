from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="Book Search API")

# To run the server for the API:
# fastapi dev app/main.py

# To view the API documentation:
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

