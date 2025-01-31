from fastapi import FastAPI
from app.api.routes import router
from mangum import Mangum

app = FastAPI()

app.include_router(router)

# Create adapter to make app compatible with AWS Lambda
handler = Mangum(app)
