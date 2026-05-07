from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional, List
from datetime import datetime
import statistics

def get_device_data(db: Session, device_id: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    query = db.query(models.DataPoint).filter(models.DataPoint.device_id == device_id)
    if start_date:
        query = query.filter(models.DataPoint.timestamp >= start_date)
    if end_date:
        query = query.filter(models.DataPoint.timestamp <= end_date)
    return query.all()

def analyze_data(data_points: List[models.DataPoint]) -> schemas.AnalysisResult:
    values = [dp.x for dp in data_points]  # анализ по оси X
    if not values:
        return schemas.AnalysisResult(min=0, max=0, count=0, sum=0, median=0)
    
    return schemas.AnalysisResult(
        min=min(values),
        max=max(values),
        count=len(values),
        sum=sum(values),
        median=statistics.median(values)
    )

def get_data_points(
    db: Session,
    device_id: str,
    skip: int = 0,
    limit: int = 100
):
    return db.query(models.DataPoint)\
        .filter(models.DataPoint.device_id == device_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
