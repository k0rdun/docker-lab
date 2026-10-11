from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    year: int = Field(..., ge=1, le=9999)

    model_config = ConfigDict(str_strip_whitespace=True)


class BookResponse(BookCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
