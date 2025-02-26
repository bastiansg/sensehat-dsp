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

from .utils import next_color


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

    @threaded
    def start_slow_intermittent_image(
        self,
        image_name: str,
        colour: tuple[int, int, int],
        refresh_rate: float = 0.005,
    ) -> None:
        self.mutex.acquire()

        image_mask = self.image_map[image_name]
        image_mask[image_mask > 0] = 1

        init_r, init_g, init_b = colour
        r = init_r
        g = init_g
        b = init_b

        transition_values = []
        while max((r, g, b)) > 50:
            r = max((r - 1), 0)
            g = max((g - 1), 0)
            b = max((b - 1), 0)
            transition_values.append((r, g, b))

        self.intermittent_image_run = True
        while self.intermittent_image_run:
            self.sense_hat.set_pixels(image_mask * [r, g, b])
            sleep(refresh_rate)

            for r_, g_, b_ in transition_values:
                if not self.intermittent_image_run:
                    continue

                self.sense_hat.set_pixels(image_mask * [r_, g_, b_])
                sleep(refresh_rate)

            for r_, g_, b_ in reversed(transition_values):
                if not self.intermittent_image_run:
                    continue

                self.sense_hat.set_pixels(image_mask * [r_, g_, b_])
                sleep(refresh_rate)

        self.mutex.release()

    @threaded
    def start_color_cycle(self, image_name: str):
        self.mutex.acquire()
        r, g, b = (255, 0, 0)
        image_mask = self.image_map[image_name]
        image_mask[image_mask > 0] = 1
        while True:
            r, g, b = next_color(r, g, b)
            self.sense_hat.set_pixels(image_mask * [r, g, b])
            sleep(0.001)

        self.clear()
        self.mutex.release()

    def set_image(self, image_name: str) -> None:
        self.mutex.acquire()
        self.sense_hat.set_pixels(pixel_list=self.image_map[image_name])
        self.mutex.release()
