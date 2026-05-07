from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from . import crud, schemas, models, tasks
from .database import get_db

router = APIRouter()

@router.get("/data/{device_id}", response_model=dict)
async def get_device_data(
    device_id: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> dict:
    # Получаем данные из БД через CRUD-функцию
    data_points = crud.get_data_points(db, device_id=device_id, skip=skip, limit=limit)

    # Форматируем ответ в нужном виде
    response_data = {
        "device_id": device_id,
        "data": [
            {
                "timestamp": point.timestamp.isoformat(),
                "x": point.x,
                "y": point.y,
                "z": point.z
            }
            for point in data_points
        ],
        "count": len(data_points)
    }

    return response_data

@router.get("/data/{device_id}")
async def get_device_data(device_id: str):
    return {
        "device_id": device_id,
        "data": [
            {"timestamp": "2023-10-01T10:00:00", "x": 1.5, "y": 2.3, "z": 0.8},
            {"timestamp": "2023-10-01T10:01:00", "x": 1.6, "y": 2.1, "z": 0.9}
        ],
        "count": 2
    }

@router.get("/analyze/{device_id}", response_model=schemas.AnalysisResult)
async def analyze_device(
    device_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Асинхронный анализ данных устройства за указанный период.
    Результаты возвращаются после выполнения задачи Celery.
    """
    task = tasks.analyze_device_data_async.delay(device_id, start_date, end_date)
    try:
        result = task.get(timeout=30)  # ожидание результата до 30 секунд
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при анализе данных: {str(e)}"
        )

@router.post("/users/", response_model=schemas.UserCreate)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Создание нового пользователя."""
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/devices/", response_model=schemas.DeviceCreate)
async def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """Привязка устройства к пользователю."""
    # Проверка существования пользователя
    user = db.query(models.User).filter(models.User.id == device.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    db_device = models.Device(
        user_id=device.user_id,
        device_id=device.device_id
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.get("/users/{user_id}/analysis", response_model=dict)
async def get_user_analysis(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Анализ данных всех устройств пользователя:
    - агрегированные результаты по всем устройствам;
    - детализация по каждому устройству.
    """
    # Получаем все устройства пользователя
    devices = db.query(models.Device).filter(models.Device.user_id == user_id).all()
    if not devices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Устройства пользователя не найдены"
        )
    
    # Агрегированный результат
    all_data = []
    for device in devices:
        device_data = crud.get_device_data(db, device.device_id, start_date, end_date)
        all_data.extend(device_data)
    
    aggregated_result = crud.analyze_data(all_data)
    
    # Результаты по каждому устройству
    per_device_results = {}
    for device in devices:
        device_data = crud.get_device_data(db, device.device_id, start_date, end_date)
        per_device_results[device.device_id] = crud.analyze_data(device_data)
    
    return {
        "aggregated": aggregated_result,
        "per_device": per_device_results
    }

@router.get("/devices/{device_id}/data", response_model=List[schemas.DataPointResponse])
async def get_device_data(
    device_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получение сырых данных устройства с пагинацией."""
    data_points = crud.get_device_data(db, device_id, start_date, end_date)
    return data_points[skip:skip + limit]
