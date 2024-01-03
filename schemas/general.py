from pydantic import BaseModel

class HTTPErrorModel(BaseModel):
    detail: str
    class Config:
        schema_extra = {
            "example": { "detail": "string" },
        }

class PingModel(BaseModel):
    message: str
    class Config:
        schema_extra = {
            "example": { "message": "pong" },
        }
