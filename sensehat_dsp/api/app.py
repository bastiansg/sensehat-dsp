from common.logger import get_logger
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from routers.set_image import set_image_router
from routers.clear_image import clear_image_router
from routers.intermittent_image import (
    start_intermittent_image_router,
    stop_intermittent_image_router,
)

from routers.slow_intermittent_image import start_slow_intermittent_image_router


logger = get_logger(__name__)


app = FastAPI()
router = APIRouter()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.get("/", include_in_schema=False)(lambda: RedirectResponse(url="/docs/"))


@app.get("/healthcheck", tags=["status"])
def healthcheck():
    return {"status": "ok"}


app.include_router(set_image_router)
app.include_router(clear_image_router)

app.include_router(start_intermittent_image_router)
app.include_router(start_slow_intermittent_image_router)
app.include_router(stop_intermittent_image_router)
