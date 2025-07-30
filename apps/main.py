import os
import random

import qrcode
from fastapi import APIRouter, Depends
from uuid import uuid4
from db.models import Game, Question, Option
from db.sessions import SessionDep
from instruments.forms import GameForm, QuestionForm, OptionForm
from instruments.login import get_current_user

main = APIRouter()

MEDIA_ROOT = "media/qr_codes"
MEDIA_URL = "/media/qr_codes"

os.makedirs(MEDIA_ROOT, exist_ok=True)


@main.post("/create/game/")
async def save_game(
        form: GameForm,
        session: SessionDep,
        current_user: dict = Depends(get_current_user)
):
    # 1. Game code generatsiya qilinadi
    code = str(random.randrange(5 ** 5, 6 ** 5))

    # 2. QR code yaratamiz
    qr_data = f"http:localhost:8000/join/{code}"  # yoki boshqa ma’lumot
    qr_img = qrcode.make(qr_data)

    filename = f"{uuid4()}.png"
    filepath = os.path.join(MEDIA_ROOT, filename)
    qr_img.save(filepath)

    # 3. Game obyektini yaratamiz
    game = await Game.create(
        session,
        **dict(form),
        code=code,
        user_id=current_user.id,
        qr_code_path=f"{MEDIA_URL}/{filename}"  # Modelga saqlab qo‘yamiz (agar kerak bo‘lsa)
    )

    # 4. Response
    return {
        "id": game.id,
        "code": code,
        "qr_code_url": f"http://localhost:8000{MEDIA_URL}/{filename}"  # frontendga ko‘rsatish uchun
    }


@main.get('/games/list/', response_model=list[Game])
async def get_games(session: SessionDep, current_user: dict = Depends(get_current_user)):
    games = await Game.get_all(session)
    return games


@main.post('/create/question/')
async def create_question(form: QuestionForm, session: SessionDep):
    question = await Question.create(session, **dict(form))
    return question


@main.post('/create/options')
async def create_options(form: OptionForm, session: SessionDep):
    options = await Option.create(session, **dict(form))
    return options


@main.get('/questions/list/{pk}', response_model=list[Question])
async def get_questions(session: SessionDep, pk: int):
    game = await Game.get(session, Game.code, str(pk))
    questions = await Question.get(session, Question.game_id, game.id, True)
    return questions


@main.get('/options/list/{pk}', response_model=list[Option])
async def get_options(session: SessionDep, pk: int):
    options = await Option.get(session, Option.question_id, pk, True)
    return options
