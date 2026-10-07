from pydantic import BaseModel, model_validator
from typing import Optional

class PredictRequest(BaseModel):
    subject: Optional[str] = ""
    body: str
    
    @model_validator(mode='after')
    def check_empty(self):
        subject_val = self.subject.strip() if self.subject else ""
        body_val = self.body.strip() if self.body else ""
        if not subject_val and not body_val:
            raise ValueError("Email subject and body cannot both be empty.")
        return self

class PredictResponse(BaseModel):
    prediction: str
    confidence: float
    message: str
