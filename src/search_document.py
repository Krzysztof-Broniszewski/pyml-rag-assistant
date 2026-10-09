from pydantic import BaseModel, Field, HttpUrl

class SearchDocument(BaseModel):
    id: str = Field(min_lenght=1)
    content: str = Field(min_lenght=1)
    source: str = Field(min_lenght=1)
    url: HttpUrl
    content_vector: list[float] = Field(min_length=1536, max_length=1536)