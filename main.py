from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles

from apps import main, socket, login_register
from db import engine
from db.models import metadata

app = FastAPI(title="User API")

app.include_router(main, prefix="/api", tags=["api"])
app.include_router(socket, prefix='/socket', tags=["socket"])
app.include_router(login_register, prefix="/login", tags=["login"])

app.mount("/media", StaticFiles(directory="media"), name="media")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="My API with JWT Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token/")


app.openapi = custom_openapi
