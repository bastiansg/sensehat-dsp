from pydantic import BaseModel, Field, validator, PositiveFloat, StrictStr

from sensehat_dsp.display.dsp_images import dsp_images


DSP_NAMES = [img["name"] for img in dsp_images]


class Image(BaseModel):
    name: StrictStr = Field(
        description="image to be displayed",
        example="space-invader-1",
    )

    @validator("name")
    def name_validator(cls, v):
        if v not in DSP_NAMES:
            raise ValueError(
                f"invalid image name: {v}, valid names: {DSP_NAMES}"
            )

        return v


class IntermittentImage(BaseModel):
    name: StrictStr = Field(
        description="image to be displayed",
        example="space-invader-1",
    )

    refresh_rate: PositiveFloat = Field(
        description="blink interval in seconds",
        example=0.5,
    )

    @validator("name")
    def name_validator(cls, v):
        if v not in DSP_NAMES:
            raise ValueError(
                f"invalid image name: {v}, valid names: {DSP_NAMES}"
            )

        return v
