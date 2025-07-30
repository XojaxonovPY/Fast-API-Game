from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from db import engine
from db.models import User, Game, Question, Answer, Player, Option
from web.provider import UsernameAndPasswordProvider

app = Starlette()
admin = Admin(engine,
              title='P_29Admin',
              base_url='/',
              auth_provider=UsernameAndPasswordProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key="sdgfhjhhsfdghn")]
              )
admin.add_view(ModelView(User))
admin.add_view(ModelView(Game))
admin.add_view(ModelView(Question))
admin.add_view(ModelView(Answer))
admin.add_view(ModelView(Player))
admin.add_view(ModelView(Option))
admin.mount_to(app)


import bcrypt

print(bcrypt.hashpw("3".encode(), salt=bcrypt.gensalt()))

