from typing import Literal
from fastapi import APIRouter
from pydantic import BaseModel, Field, StrictStr, PositiveFloat


set_image_router = APIRouter()


class Image(BaseModel):
    name: Literal[
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
    refresh_rate: PositiveFloat = 1.0


class Status(BaseModel):
    status: StrictStr
