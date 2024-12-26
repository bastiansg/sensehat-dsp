from fastapi import APIRouter

from .utils import get_display
from .meta import IntermittentImage, Status


start_intermittent_image_router = APIRouter()
stop_intermittent_image_router = APIRouter()


@start_intermittent_image_router.post(
    "/sensehat_dsp/start_intermittent_image",
    tags=["intermittent_image"],
)
async def start_intermittent_image(image: IntermittentImage) -> Status:
    dsp = get_display()
    dsp.start_intermittent_image(
        image_name=image.name,
        refresh_rate=image.refresh_rate,
    )

    return Status(status="ok")


@stop_intermittent_image_router.post(
    "/sensehat_dsp/stop_intermittent_image",
    tags=["intermittent_image"],
)
async def stop_intermittent_image() -> Status:
    dsp = get_display()
    dsp.stop_intermittent_image()

    return Status(status="ok")
