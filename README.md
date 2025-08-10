# 🎮 Fast-API-Game

## 📌 Loyihaning qisqacha tavsifi

**Fast-API-Game** — bu FastAPI yordamida yaratilgan o'yin ilovasi bo'lib, foydalanuvchilarga o'yinlar bilan bog'liq
ma'lumotlarni taqdim etadi. Ushbu loyiha Python dasturlash tili va FastAPI web freymorkidan foydalangan holda ishlab
chiqilgan.

## ⚙️ Asosiy xususiyatlar

- **FastAPI**: Yuqori samaradorlikka ega web freymorki.
- **WebSocket**: Real-vaqtda ulanish va xabar almashish imkoniyati.
- **Docker**: Ilovani konteynerlash va uni turli muhitlarda ishlatish imkonini beradi.
- **Alembic**: Ma'lumotlar bazasidagi o'zgarishlarni boshqarish uchun migratsiya vositasi.
- **pytest**: Testlarni yozish va bajarish uchun vosita.

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
alembic upgrade head
```

5. Ilovani ishga tushirish

```bash
uvicorn main:app --reload
```

Ilova http://127.0.0.1:8000 manzilida ishga tushadi.

## 🧪 Testlarni bajarish

```bash
pytest
```

## 📄 Litsenziya

Loyiha MIT litsenziyasi asosida tarqatiladi.
