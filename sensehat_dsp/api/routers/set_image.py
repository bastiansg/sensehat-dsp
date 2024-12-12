from fastapi import APIRouter

from .utils import get_display
from .meta import Image, Status


set_image_router = APIRouter()


@set_image_router.post("/sensehat_dsp/set_image")
async def set_image(image: Image) -> Status:
    dsp = get_display()
    dsp.set_image(image_name=image.name)

    return Status(status="ok")
