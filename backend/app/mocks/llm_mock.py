# llm_mock.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RefineRequest(BaseModel):
    query: str

class EnhanceRequest(BaseModel):
    books: list

@app.post("/refine")
async def refine_endpoint(request: RefineRequest):
    # For testing, simply append " refined" to the query.
    return {"refined_query": request.query + " refined"}

@app.post("/enhance")
async def enhance_endpoint(request: EnhanceRequest):
    # For testing, append " (enhanced)" to each book's description.
    enhanced_books = []
    for book in request.books:
        if "description" in book:
            book["description"] += " (enhanced)"
        enhanced_books.append(book)
    return {"enhanced_books": enhanced_books}