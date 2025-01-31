from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from mangum import Mangum

from app.api.routes import router

app = FastAPI()
app.include_router(router)

handler = Mangum(app)

@app.get("/")
async def health_check(param: str = Query(None, description="Sample query parameter")):
    """
    AWS Lambda-compatible GET endpoint.
    Accepts query parameters and returns a JSON response.
    """
    return {"status": "ok", "data": param}

# @app.post("/test")
# async def test(request: Request):
#     request_info = await request.json()
#     return {"status": "ok", "data": request_info}



# Create the Lambda handler
# handler = Mangum(app)

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.routes import router

# app = FastAPI(title="Book Search API")

# # To run the server forfastapi dev app/main.py
# # http://127.0.0.1:8000/docs
# # http://127.0.0.1:8000/redoc

# # Add CORS Middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["http://localhost:3000"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# app.include_router(router)
