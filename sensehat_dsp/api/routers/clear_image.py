from fastapi import APIRouter
from pydantic import BaseModel, StrictStr

from .utils import get_display


clear_image_router = APIRouter()


class ClearImageOutput(BaseModel):
    status: StrictStr


@clear_image_router.post("/sensehat_dsp/image/clear")
async def clear_image() -> ClearImageOutput:
    dsp = get_display()
    dsp.clear()

    return ClearImageOutput(status="ok")
