from fastapi import APIRouter

from .utils import get_display
from .meta import DisplayImage, Status


start_intermittent_image_router = APIRouter()


@start_intermittent_image_router.post("/sensehat_dsp/start_intermittent_image")
async def start_intermittent_image(image: DisplayImage) -> Status:
    dsp = get_display()
    if dsp.is_active:
        return Status(status="busy")

    dsp.start_intermittent_image(
        image_name=image.name,
        refresh_rate=image.refresh_rate,
    )

    return Status(status="ok")
