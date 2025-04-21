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

from sensehat_dsp.gol import GOL
from common.logger import get_logger

from .utils import next_color
from .dsp_images import dsp_images, ImageName


logger = get_logger(__name__)


F = TypeVar("F", bound=Callable[..., None])


# TODO: Move this fucntion to common
def threaded(func: Callable[..., None]) -> Callable[..., None]:
    def wrapper(*args: Any, **kwargs: Any) -> None:
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    return wrapper


class Color(BaseModel):
    r: NonNegativeInt = Field(le=255, default=255)
    g: NonNegativeInt = Field(le=255, default=255)
    b: NonNegativeInt = Field(le=255, default=255)


class Image(BaseModel):
    name: StrictStr
    image: list[NonNegativeInt] = Field(len=64)
    p_color: Color = Field(description="Primary color.")
    s_color: Color = Field(description="Secundary color.")


class Display:
    def __init__(
        self,
        images: list[Image] = dsp_images,
        initial_rotation: int = 180,
        refresh_rate: float = 1.0,
    ):
        self.sense_hat = SenseHat()
        self.initial_rotation = initial_rotation

        self.clear()
        self.mutex = Lock()
        self.is_active = False

        images = [Image(**img) for img in images]
        self.image_map = self.get_image_map(images=images)

        self.gol = GOL()
        self.refresh_rate = refresh_rate

    def stop(self) -> None:
        self.is_active = False

    def clear(self) -> None:
        self.sense_hat.clear()
        self.sense_hat.set_rotation(self.initial_rotation)

    @staticmethod
    def get_np_image(image: Image) -> np.ndarray:
        return np.array(
            [
                [
                    image.p_color.r,
                    image.p_color.g,
                    image.p_color.b,
                ]
                if pixel
                else [
                    image.s_color.r,
                    image.s_color.g,
                    image.s_color.b,
                ]
                for pixel in image.image
            ]
        )

    @staticmethod
    def get_image_map(images: list[Image]) -> dict:
        return {
            image.name: Display.get_np_image(image=image) for image in images
        }

    @threaded
    def start_intermittent_image(
        self,
        image_name: ImageName,
        refresh_rate: float = 0.5,
    ) -> None:
        self.mutex.acquire()

        self.refresh_rate = refresh_rate
        self.is_active = True
        while self.is_active:
            self.sense_hat.set_pixels(self.image_map[image_name])
            sleep(self.refresh_rate)
            self.clear()
            sleep(self.refresh_rate)

        self.mutex.release()

    @threaded
    def start_color_cycle(
        self,
        image_name: ImageName,
        refresh_rate: float = 0.001,
    ) -> None:
        self.mutex.acquire()
        r, g, b = (255, 0, 0)
        image = self.image_map[image_name]
        image_mask = np.array(
            [
                [1, 1, 1] if value > 0 else [0, 0, 0]
                for value in np.sum(image, axis=1)
            ]
        )

        self.refresh_rate = refresh_rate
        self.is_active = True
        while self.is_active:
            r, g, b = next_color(r, g, b)
            self.sense_hat.set_pixels(image_mask * [r, g, b])
            sleep(self.refresh_rate)

        self.mutex.release()

    @threaded
    def start_gol(
        self,
        p_color: Color,
        s_color: Color,
        refresh_rate: float = 0.5,
    ) -> None:
        self.mutex.acquire()
        gol_grids = self.gol.get_grids()

        self.refresh_rate = refresh_rate
        self.is_active = True
        while self.is_active:
            image = Image(
                name="gol",
                image=next(gol_grids).squeeze().flatten().int().tolist(),
                p_color=p_color,
                s_color=s_color,
            )

            self.sense_hat.set_pixels(pixel_list=self.get_np_image(image=image))
            sleep(self.refresh_rate)

        self.mutex.release()

    def set_image(self, image_name: str) -> None:
        self.mutex.acquire()
        self.sense_hat.set_pixels(pixel_list=self.image_map[image_name])
        self.mutex.release()
