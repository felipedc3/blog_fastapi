from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from src.controllers import post, auth
from src.database import database, metadata, engine
from src.exceptions import NotFoundPostError



@asynccontextmanager
async def lifespan(app: FastAPI):
    from models.post import posts  #noqa
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(post.router)

@app.exception_handler(NotFoundPostError)
async def not_found_post_exception_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )