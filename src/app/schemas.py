from typing import List, Optional
from pydantic import BaseModel


class ApplicantSchema(BaseModel):
    snils: str
    code: Optional[str]
    university: str
    score: Optional[str]
    origin: str
    position: Optional[str]


class ApplicantsSchema(BaseModel):
    items: List[ApplicantSchema]