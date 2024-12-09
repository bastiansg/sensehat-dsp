from sense_hat import SenseHat
from functools import lru_cache

from sensehat_dsp.display import Image, Display, dsp_images


@lru_cache(maxsize=1)
def get_display() -> Display:
    sense_hat = SenseHat()
    return Display(
        sense_hat=sense_hat,
        images=[Image(**img) for img in dsp_images],
    )
