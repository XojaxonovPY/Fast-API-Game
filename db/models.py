import asyncio

from sqlalchemy import String, Integer, Text
from sqlmodel import Field, SQLModel, Relationship

from db import engine
from db.config import CreatedModel


class User(CreatedModel, table=True):
    name: str = Field(sa_type=String, nullable=True)
    email: str = Field(sa_type=String)
    password: str = Field(sa_type=String)

    games: list['Game'] = Relationship(back_populates='user')


class Game(CreatedModel, table=True):
    title: str = Field(sa_type=String)
    code: str = Field(sa_type=String)
    user_id: int = Field(foreign_key='users.id', ondelete='CASCADE')
    qr_code:str=Field(sa_type=Text, nullable=True)


    questions: list['Question'] = Relationship(back_populates='game')
    user: 'User' = Relationship(back_populates='games')
    players: list['Player'] = Relationship(back_populates='game')


class Question(CreatedModel, table=True):
    text: str = Field(sa_type=String)
    correct_answer: str = Field(sa_type=String)
    ball: int = Field(sa_type=Integer, default=0)
    game_id: int = Field(foreign_key='games.id', ondelete='CASCADE')

    game: 'Game' = Relationship(back_populates='questions')
    options: list['Option'] = Relationship(back_populates='question')


class Option(CreatedModel, table=True):
    text: str = Field(sa_type=String)
    question_id: int = Field(foreign_key='questions.id', ondelete='CASCADE')

    question: 'Question' = Relationship(back_populates='options')


class Player(CreatedModel, table=True):
    name: str = Field(sa_type=String, nullable=True)
    balance: int = Field(sa_type=Integer, default=0)
    game_id: int = Field(foreign_key='games.id', ondelete='CASCADE')

    game: 'Game' = Relationship(back_populates='players')
    answers: list['Answer'] = Relationship(back_populates='player')


class Answer(CreatedModel, table=True):
    text: str = Field(sa_type=String)
    player_id: int = Field(foreign_key='players.id', ondelete='CASCADE')

    player: 'Player' = Relationship(back_populates='answers')


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


metadata = SQLModel.metadata

if __name__ == "__main__":
    asyncio.run(create_db_and_tables())
