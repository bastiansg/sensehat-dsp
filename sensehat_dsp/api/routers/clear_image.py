from fastapi import APIRouter
from pydantic import BaseModel, StrictStr

from .utils import get_display


clear_image_router = APIRouter()


class ClearImageOutput(BaseModel):
    status: StrictStr


@clear_image_router.post("/sensehat_dsp/clear")
async def clear() -> ClearImageOutput:
    dsp = get_display()
    dsp.stop_intermittent_image()
    dsp.clear()

    return ClearImageOutput(status="ok")
