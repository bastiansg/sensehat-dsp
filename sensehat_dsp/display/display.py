import numpy as np

from time import sleep
from pydantic import (
    BaseModel,
    StrictStr,
    NonNegativeInt,
    Field,
)


from sense_hat import SenseHat
from threading import Thread, Lock
from typing import Callable, TypeVar, Any

from common.logger import get_logger


logger = get_logger(__name__)


F = TypeVar("F", bound=Callable[..., None])


def threaded(func: Callable[..., None]) -> Callable[..., None]:
    def wrapper(*args: Any, **kwargs: Any) -> None:
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    return wrapper


# TODO: Validate image, d_color and l_color values.
class Image(BaseModel):
    name: StrictStr
    image: list[NonNegativeInt] = Field(len=64)
    d_color: list[NonNegativeInt] = Field(len=3)
    l_color: list[NonNegativeInt] = Field(len=3)


class Display:
    def __init__(
        self,
        sense_hat: SenseHat,
        images: list[Image],
        initial_rotation: int = 180,
    ):
        self.sense_hat = sense_hat
        self.initial_rotation = initial_rotation

        self.clear()
        self.mutex = Lock()
        self.image_map = self.get_image_map(images=images)

    def clear(self) -> None:
        self.sense_hat.clear()
        self.sense_hat.set_rotation(self.initial_rotation)

    def get_np_image(self, image: Image) -> np.ndarray:
        return np.array(
            [image.d_color if pixel else image.l_color for pixel in image.image]
        )

    def get_image_map(self, images: list[Image]) -> dict:
        return {image.name: self.get_np_image(image=image) for image in images}

    @threaded
    def start_intermittent_image(
        self,
        image_name: str,
        refresh_rate: float,
    ) -> None:
        self.mutex.acquire()

        self.intermittent_image_run = True
        while self.intermittent_image_run:
            self.sense_hat.set_pixels(self.image_map[image_name])
            sleep(refresh_rate)
            self.clear()
            sleep(refresh_rate)

        self.mutex.release()

    def stop_intermittent_image(self):
        self.intermittent_image_run = False

    def set_image(self, image_name: str) -> None:
        self.mutex.acquire()
        self.sense_hat.set_pixels(pixel_list=self.image_map[image_name])
        self.mutex.release()
