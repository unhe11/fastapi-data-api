from fastapi import FastAPI
from app.routes import router

app = FastAPI()

# Корневой маршрут — должен быть объявлен ДО подключения роутера
@app.get("/")
async def root():
    return {"message": "API is running"}

# Подключение роутера с префиксом
app.include_router(router, prefix="/api/v1", tags=["api"])