from fastapi import APIRouter
from pydantic import BaseModel, StrictStr

from .utils import get_display


clear_display_router = APIRouter()


class ClearImageOutput(BaseModel):
    status: StrictStr


@clear_display_router.post("/sensehat_dsp/clear_display")
async def clear_display() -> ClearImageOutput:
    dsp = get_display()

    dsp.is_active = False
    dsp.clear()

    return ClearImageOutput(status="ok")
