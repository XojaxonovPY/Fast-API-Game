from pydantic import BaseModel, model_validator, field_validator, EmailStr, Field


class LoginForm(BaseModel):
    email: EmailStr = None
    password: str = None


class RegisterForm(BaseModel):
    email: EmailStr = None
    password: str = None


class VerifyForm(BaseModel):
    pk: str = None
    code: str = None



class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = {
        "from_attributes": True
    }


class GameForm(BaseModel):
    title: str = None


class OptionForm(BaseModel):
    text: str = None
    question_id: int = None


class QuestionForm(BaseModel):
    text: str = None
    correct_answer: str = None
    game_id: int = None
