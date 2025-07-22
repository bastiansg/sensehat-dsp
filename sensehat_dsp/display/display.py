import numpy as np

from time import sleep
from pydantic import (
    BaseModel,
    StrictStr,
    NonNegativeInt,
    Field,
)

from threading import Lock
from sense_hat import SenseHat

from sensehat_dsp.gol import GOL
from common.logger import get_logger
from common.utils.threading import threaded

from .utils import next_color


logger = get_logger(__name__)


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
        initial_rotation: int = 180,
        refresh_rate: float = 1.0,
    ):
        self.sense_hat = SenseHat()
        self.initial_rotation = initial_rotation

        self.clear()
        self.mutex = Lock()
        self.is_active = False

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

    @threaded
    def start_intermittent_image(
        self,
        image: Image,
        refresh_rate: float = 0.5,
    ) -> None:
        self.mutex.acquire()

        np_image = self.get_np_image(image=image)
        self.refresh_rate = refresh_rate
        self.is_active = True
        while self.is_active:
            self.sense_hat.set_pixels(np_image)
            sleep(self.refresh_rate)
            self.clear()
            sleep(self.refresh_rate)

        self.mutex.release()

    @threaded
    def start_color_cycle(
        self,
        image: Image,
        refresh_rate: float = 0.001,
    ) -> None:
        self.mutex.acquire()
        r, g, b = (255, 0, 0)
        np_image = self.get_np_image(image=image)
        image_mask = np.array(
            [
                [1, 1, 1] if value > 0 else [0, 0, 0]
                for value in np.sum(np_image, axis=1)
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

    @threaded
    def start_image_sequence(
        self,
        images: list[Image],
        refresh_rate: float = 0.5,
    ) -> None:
        self.mutex.acquire()
        self.refresh_rate = refresh_rate
        self.is_active = True
        while self.is_active:
            for image in images:
                np_image = self.get_np_image(image=image)
                self.sense_hat.set_pixels(np_image)
                sleep(self.refresh_rate)

        self.mutex.release()

    def set_image(self, image: Image) -> None:
        self.mutex.acquire()
        np_image = self.get_np_image(image=image)
        self.sense_hat.set_pixels(pixel_list=np_image)
        self.mutex.release()
