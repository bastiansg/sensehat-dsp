from pydantic import BaseModel, Field


class Image(BaseModel):
    image_name: str = Field(
        description="image to be displayed",
        example="space-invader-1"
    )

class IntermittentImage(BaseModel):
    image_name: str = Field(
        description="image to be displayed",
        example="space-invader-1"
    )

    refresh_rate: float = Field(
        description="blink interval in seconds",
        example=0.5
    )
