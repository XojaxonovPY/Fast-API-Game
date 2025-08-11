# 🎮 Fast-API-Game

## 📌 Loyihaning qisqacha tavsifi

**Fast-API-Game** — bu FastAPI yordamida yaratilgan o'yin ilovasi bo'lib, foydalanuvchilarga o'yinlar bilan bog'liq
ma'lumotlarni taqdim etadi. Ushbu loyiha Python dasturlash tili va FastAPI web freymorkidan foydalangan holda ishlab
chiqilgan va [**Kahoot**](https://kahoot.com/) — web-saytiga o‘xshatib yaratilgan.

## ⚙️ Asosiy xususiyatlar

- **FastAPI**: Yuqori samaradorlikka ega web freymorki.
- **WebSocket**: Real-vaqtda ulanish va xabar almashish imkoniyati.
- **Docker**: Ilovani konteynerlash va uni turli muhitlarda ishlatish imkonini beradi.
- **SQLAlchemy**:Python ORM Bilan (asyns) tarzda ishlaydi va DB bilan malumot almashish tezroq boladi.
- **Alembic**: Ma'lumotlar bazasidagi o'zgarishlarni boshqarish uchun migratsiya vositasi.
- **Starlette Admin**: Starlette yoki FastAPI asosida ma’lumotlar bazasi uchun admin panel yaratish vositasi.
- **pytest**: Testlarni yozish va bajarish uchun vosita.


## 🛠 Texnologiyalar

| Texnologiya      | Tavsifi                                                       |
|------------------|---------------------------------------------------------------|
| Python 3.12      | Asosiy dasturlash tili                                        |
| FAST API         | Backend API yaratish freymvorki                               |
| PostgreSQL       | Ma’lumotlar bazasi                                            |
| WebSocket        | Real-time ulanish                                             |
| Docker           | Konteynerizatsiya                                             |
| Redis            | Kesh va xabar brokeri                                         |
| Celery           | Fon vazifalarni asinxron bajarish va periodik ishlar          |
| SQLAlchemy       | Python ORM va SQL toolkiti, DB bilan obyektlar orqali ishlash |



## 🛠️ O'rnatish va ishga tushirish

1. Repositoriyani klonlash

```bash
git clone https://github.com/XojaxonovPY/Fast-API-Game.git
cd Fast-API-Game
```

2. Virtual muhit yaratish va kutubxonalarni o'rnatish

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Docker yordamida ishga tushirish

```bash
docker-compose up --build
```

4. Ma'lumotlar bazasini migratsiya qilish

```bash
alembic revision --autogenerate -m "Create a baseline migrations" && alembic upgrade head
```

5. Ilovani ishga tushirish

```bash
uvicorn main:app --reload
```

6. Admin panelni ishga tushirish

```bash
uvicorn web.app:app --host localhost --port 8000
```

Ilova http://127.0.0.1:8000 manzilida ishga tushadi.

## 🧪 Testlarni bajarish

```bash
pytest
```

## ENV File konfiguratsiyasi
```env
DB_URL=postgresql+asyncpg://db_name:password@host:port/db_name
EMAIL_FROM=your_email
EMAIL_PASSWORD=your_password
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password
REDIS_URL=redis://host:port/0
```

## 📊 Ma’lumotlar bazasi modeli

[DrawSQL’da model sxemasini ko‘rish](https://drawsql.app/teams/gayrat-1/diagrams/fast-api-game)

## 📄 Litsenziya

Loyiha MIT litsenziyasi asosida tarqatiladi.
