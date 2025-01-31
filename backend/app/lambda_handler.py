from mangum import Mangum
from app.main import app


# Mangum adapter makes FastAPI work on AWS Lambda
handler = Mangum(app)
