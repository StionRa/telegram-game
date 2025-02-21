from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

# Файл базы данных
DB_FILE = "backend/users.json"

# Создаем файл, если его нет
if not os.path.exists(DB_FILE) or os.stat(DB_FILE).st_size == 0:
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

# Модели данных
class User(BaseModel):
    id: int
    first_name: str
    username: str

class UserID(BaseModel):
    id: int

class UpdateStats(BaseModel):
    id: int
    strength: int
    dexterity: int
    endurance: int
    intelligence: int

# Регистрация нового пользователя
@app.post("/register")
async def register_user(user: User):
    with open(DB_FILE, "r") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            users = {}

    user_id = str(user.id)

    if user_id not in users:
        users[user_id] = {
            "first_name": user.first_name,
            "username": user.username,
            "character": {
                "name": "Герой без имени",
                "level": 1,
                "progress": 0,
                "gold": 100,
                "crypto": 0,
                "strength": 5,
                "dexterity": 5,
                "endurance": 5,
                "intelligence": 5
            }
        }

        with open(DB_FILE, "w") as f:
            json.dump(users, f, indent=4)

        return {"status": "new_user", "message": f"Пользователь {user.username} зарегистрирован"}

    return {"status": "existing_user", "message": f"Пользователь {user.username} уже есть в базе"}

# Получение данных персонажа
@app.post("/get_character")
async def get_character(user: UserID):
    with open(DB_FILE, "r") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            return {"status": "error", "message": "Файл базы данных поврежден"}

    user_id = str(user.id)
    if user_id in users and users[user_id].get("character"):
        return {"status": "success", "character": users[user_id]["character"]}

    return {"status": "error", "message": "Персонаж не найден"}

# Обновление характеристик персонажа
@app.post("/update_character")
async def update_character(stats: UpdateStats):
    with open(DB_FILE, "r") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            return {"status": "error", "message": "Файл базы данных поврежден"}

    user_id = str(stats.id)
    if user_id in users and "character" in users[user_id]:
        users[user_id]["character"].update({
            "strength": stats.strength,
            "dexterity": stats.dexterity,
            "endurance": stats.endurance,
            "intelligence": stats.intelligence
        })
        with open(DB_FILE, "w") as f:
            json.dump(users, f, indent=4)
        return {"status": "success", "message": "Характеристики обновлены"}
    
    return {"status": "error", "message": "Персонаж не найден"}

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
