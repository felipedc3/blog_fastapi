from pydantic import BaseModel, field_validator
from datetime import datetime, timezone



class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published_at: datetime | None

    @field_validator('published_at', mode='before')
    @classmethod
    def add_timezone(cls, v):
        if v is not None and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v
    