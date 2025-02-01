from pydantic import BaseModel
from typing import List, Any, Optional

class OpenLibraryResponse(BaseModel):
    numFound: int
    start: int
    numFoundExact: bool
    num_found: int
    documentation_url: str
    q: str
    offset: Optional[Any]  
    docs: List[Any]        