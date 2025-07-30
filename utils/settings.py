from os import getenv
from dotenv import load_dotenv
from redis.asyncio import Redis

from utils.env_path import Env_path

load_dotenv(Env_path)

redis = Redis()


class Settings:
    DB_URL = getenv('DB_URL')
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_FROM = getenv('EMAIL_FROM')
    EMAIL_PASSWORD = getenv('EMAIL_PASSWORD')
    ADMIN = getenv('ADMIN')
    PASSWORD = getenv('PASSWORD')
    REDIS_URL = getenv('REDIS_URL')
    ADMIN_USERNAME=getenv('ADMIN_USERNAME')
    ADMIN_PASSWORD=getenv('ADMIN_PASSWORD')
