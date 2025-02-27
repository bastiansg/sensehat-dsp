from fastapi import APIRouter

from .utils import get_display
from .meta import ColorCycleImage, Status


start_color_cycle_router = APIRouter()


@start_color_cycle_router.post("/sensehat_dsp/start_color_cycle")
async def start_color_cycle(image: ColorCycleImage) -> Status:
    dsp = get_display()
    if dsp.is_active:
        return Status(status="busy")

    dsp.start_color_cycle(
        image_name=image.name,
        refresh_rate=image.refresh_rate,
    )

    return Status(status="ok")
