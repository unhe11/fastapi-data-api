from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DataPointCreate(BaseModel):
    x: float
    y: float
    z: float

class DataPointResponse(BaseModel):
    id: int
    device_id: str
    x: float
    y: float
    z: float
    timestamp: datetime

class AnalysisResult(BaseModel):
    min: float
    max: float
    count: int
    sum: float
    median: float

class UserCreate(BaseModel):
    username: str

class DeviceCreate(BaseModel):
    device_id: str
    user_id: int
