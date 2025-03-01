from typing import Any, Optional
from pydantic import BaseModel, field_validator

class MovieRecord(BaseModel):
    year: int|str
    title: str
    studios: str
    producers: str
    winner: bool
       
    @field_validator("winner", mode="before")
    def convert_winner(cls, v):
        if isinstance(v, str):
            if v.strip() == "" or  v.strip() == None:
                return False
            elif v.lower() == "yes":
                return True
            elif v.lower() == "no":
                return False
            else:
                raise ValueError("winner must be 'Yes' or 'No'")
        return v
    model_config = {
        "from_attributes": True
    }
class AwardedProducerResponse(BaseModel):
    producer: str
    interval: int 

class ProducerIntervalResponse(BaseModel):
    producer_with_longest_interval: AwardedProducerResponse
    producer_with_shortest_interval: AwardedProducerResponse

class ResponseModel(BaseModel):
    status_code: int
    data: Optional[Any] = None
    detail: Optional[str] = None
