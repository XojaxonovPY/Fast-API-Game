import json
import random
import uuid
from fastapi import APIRouter, Depends, HTTPException
from db.models import User
from db.sessions import SessionDep
from instruments.forms import RegisterForm, LoginForm, TokenResponse, VerifyForm
from instruments.login import create_refresh_token, verify_token, get_current_user
from instruments.login import get_user, verify_password, create_access_token, get_password_hash
from instruments.tasks import send_email_code
from utils.settings import redis

login_register = APIRouter()


@login_register.post("/user/register")
async def user_create(session: SessionDep, form: RegisterForm):
    user = dict(form)
    query = await User.get(session, User.email, user["email"])
    if query:
        raise HTTPException(status_code=400, detail='Email is alredy exists')
    user['password'] = await get_password_hash(form.password)
    pk = str(uuid.uuid4())
    random_code = str(random.randrange(10 ** 5, 10 ** 6))
    send_email_code.delay(user, random_code)
    await redis.mset({pk: json.dumps({'user': user, 'code': random_code})})
    return {'message': 'Send verify code', 'pk': pk}


@login_register.post("/user/verify", response_model=User)
async def user_verify(session: SessionDep, form: VerifyForm):
    redis_data = await redis.get(form.pk)
    if not redis_data:
        raise HTTPException(status_code=400, detail='Not verify code')
    data = json.loads(redis_data)
    code = data.get('code')
    if form.code != code:
        raise HTTPException(status_code=400, detail='Wrong code')
    user = data.get('user')
    user_data = await User.create(session, **user)
    await redis.delete(form.pk)
    return user_data


@login_register.post("/token", response_model=TokenResponse)
async def login(session: SessionDep, form_data: LoginForm):
    user = await get_user(session, form_data.email)
    verify = await verify_password(form_data.password, user.password)
    if not user or not verify:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = await create_access_token(data={"sub": user.email})
    refresh_token = await create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@login_register.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    payload = await verify_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_data = {"sub": payload["sub"]}
    new_access_token = await create_access_token(user_data)
    new_refresh_token = await create_refresh_token(user_data)
    return {"access_token": new_access_token, "refresh_token": new_refresh_token}


@login_register.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
