import numpy as np

from pydantic import (
    BaseModel,
    StrictStr,
    NonNegativeInt,
    Field,
)

# from time import sleep
from typing import Callable, TypeVar, Any

from sense_hat import SenseHat
from threading import Thread, Lock

from common.logger import get_logger
# from sensehat_dsp.meta.data_models import Image, IntermittentImage

# from .utils import next_color
# from .dsp_images import dsp_images


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
        self.images = images
        self.initial_rotation = initial_rotation

        self.clear()
        self.mutex = Lock()
        self.image_map = self.get_image_map(images=images)

    def clear(self) -> None:
        self.intermittent_image_run = False
        self.color_cycle_run = False

        self.sense_hat.clear()
        self.sense_hat.set_rotation(self.initial_rotation)

    def get_np_image(self, image: Image) -> np.ndarray:
        return np.array(
            [image.d_color if pixel else image.l_color for pixel in image.image]
        )

    def get_image_map(self, images: list[Image]) -> dict:
        return {image.name: self.get_np_image(image=image) for image in images}

    # def color_cycle(self, image: Image):
    #     self.mutex.acquire()
    #     r, g, b = (255, 0, 0)
    #     image_mask = self.images[image.name]
    #     image_mask[image_mask > 0] = 1
    #     while self.color_cycle_run:
    #         r, g, b = next_color(r, g, b)
    #         image = image_mask * [r, g, b]
    #         self.set_pixels(image)

    #     self.clear()
    #     self.mutex.release()

    # def intermittent_image(self, int_image: IntermittentImage):
    #     self.mutex.acquire()
    #     while self.intermittent_image_run:
    #         self.set_pixels(self.images[int_image.name])
    #         sleep(int_image.refresh_rate)
    #         self.clear()
    #         sleep(int_image.refresh_rate)

    #     self.mutex.release()

    # def start_intermittent_image(self, int_image: IntermittentImage):
    #     self.intermittent_image_run = True
    #     thread = Thread(
    #         target=self.intermittent_image,
    #         args=(int_image,),
    #     )

    #     thread.start()

    # def stop_intermittent_image(self):
    #     self.intermittent_image_run = False

    # def start_color_cycle(self, image: Image):
    #     self.color_cycle_run = True
    #     thread = Thread(target=self.color_cycle, args=(image,))
    #     thread.start()

    # def stop_color_cycle(self):
    #     self.color_cycle_run = False

    def set_image(self, image_name: str) -> None:
        self.mutex.acquire()
        self.sense_hat.set_pixels(pixel_list=self.image_map[image_name])
        self.mutex.release()
