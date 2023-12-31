from pydantic import BaseModel

class Message(BaseModel):
    status: int
    description: str
    details: list[str] | None = None


