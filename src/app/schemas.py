from typing import List, Optional
from pydantic import BaseModel


class ApplicantSchema(BaseModel):
    code: Optional[str]
    university: str
    score: Optional[str]
    origin: Optional[str]
    position: Optional[str]

    class Config:
        orm_mode = True
