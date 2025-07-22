from common.logger import get_logger
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware


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
