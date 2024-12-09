from typing import Literal
from fastapi import APIRouter
from pydantic import BaseModel, StrictStr, Field

from .utils import get_display


set_image_router = APIRouter()


class SetImageInput(BaseModel):
    image_name: Literal[
        "space-invader-1",
        "space-invader-1a",
        "space-invader-1b",
        "space-invader-2",
        "space-invader-3",
        "space-invader-4",
        "space-invader-5",
        "left-arrow",
        "right-arrow",
    ] = Field(examples=["space-invader-1"])


class SetImageOutput(BaseModel):
    status: StrictStr


@set_image_router.post("/sensehat_dsp/image/set")
async def set_image(set_image_input: SetImageInput) -> SetImageOutput:
    dsp = get_display()
    dsp.set_image(image_name=set_image_input.image_name)

    return SetImageOutput(status="ok")
