from pydantic import BaseModel, AwareDatetime



class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published_at: AwareDatetime | None

    