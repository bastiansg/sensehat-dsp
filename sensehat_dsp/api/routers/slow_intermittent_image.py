from fastapi import APIRouter

from .utils import get_display
from .meta import SlowIntermittentImage, Status


start_slow_intermittent_image_router = APIRouter()


@start_slow_intermittent_image_router.post(
    "/sensehat_dsp/start_slow_intermittent_image",
    tags=["intermittent_image"],
)
async def start_slow_intermittent_image(image: SlowIntermittentImage) -> Status:
    dsp = get_display()
    dsp.start_color_cycle(
        image_name=image.name,
        # colour=image.colour,
        # refresh_rate=image.refresh_rate,
    )

    return Status(status="ok")
