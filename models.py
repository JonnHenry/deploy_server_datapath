from typing import Any, Dict, Optional
from pydantic import BaseModel

class Prediction_Input(BaseModel):
    age: int
    hypertension: int 
    heart_disease: int 
    ever_married: str 
    work_type: str

class Prediction_Output(BaseModel):
    id: int
    stroke_input: Prediction_Input
    pred: int

class Message_Prediction(BaseModel):
    message: str


class Message_Error(BaseModel):
    status_code: int
    detail: Any
    headers: Optional[Dict[str, str]]