# Purpose: define what the data in message should contain for a response.

from pydantic import BaseModel, ConfigDict

class MessageCreate(BaseModel):
    content: str

class MessageUpdate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    content: str