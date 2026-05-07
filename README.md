# FastAPI Data Collection API

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://...
   cd fastapi-data-api
Создайте виртуальное окружение (опционально):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   или venv\Scripts\activate  # Windows
   ```
2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   
Запустите сервер:

   ```bash
uvicorn app.main:app --reload
Откройте Swagger UI: http://localhost:8000/docs
