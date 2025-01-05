from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel
from typing import Dict

# Создаем приложение FastAPI
app = FastAPI()

# Настраиваем конфигурацию AuthX
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_CSRF_COOKIE_NAME = "my_access_token"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

# Инициализируем AuthX с конфигурацией
security = AuthX(config=config)

# Временное хранилище пользователей
users_db: Dict[str, str] = {}  # username: password

# Модели запросов
class UserRegisterSchema(BaseModel):
    username: str
    password: str

class UserLoginSchema(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: UserRegisterSchema):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Сохраняем пользователя в базу данных
    users_db[user.username] = user.password
    return {"message": "User registered successfully"}

@app.post("/login")
def login(creds: UserLoginSchema, response: Response):
    # Проверка существования пользователя
    if creds.username not in users_db or users_db[creds.username] != creds.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # Создаем JWT токен
    token = security.create_access_token(uid=creds.username)
    # Устанавливаем токен в cookies
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME, 
        value=token, 
        httponly=True,
        samesite="Lax"
    )
    return {"access_token": token}

@app.get("/protected")
def protected_route(user=Depends(security.get_current_subject)):
    return {"message": f"Welcome, {user.uid}!"}
