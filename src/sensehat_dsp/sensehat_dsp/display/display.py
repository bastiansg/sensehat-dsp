import os

import numpy as np

from time import sleep
from sense_hat import SenseHat
from threading import Thread, Lock

from sensehat_dsp.logger import get_logger
from sensehat_dsp.utils.json_data import load_json

from .utils import next_color


logger = get_logger(__name__)


class Display(SenseHat):
    def __init__(
            self,
            image_path: str = "/resources/dsp-images/dsp-images.json",
            initial_rotation: int = 180,
        ):

        SenseHat.__init__(self)
        self.mutex = Lock()
        self.set_rotation(initial_rotation)

        logger.info("loading images")
        self.load_images(image_path)

        self.stop_all()
    
    def stop_all(self):
        self.intermittent_image_run = False
        self.color_cycle_run = False

    def parse_raw_image(
            self,
            raw_image: dict
        ) -> list[tuple[int, int, int]]:

        parsed_image = [
            raw_image["d-color"] if pixel else raw_image["l-color"]
            for pixel in raw_image["image"]
        ]

        return parsed_image

    def load_images(self, image_path: str):
        raw_images = load_json(image_path)
        self.images = {
            raw_image["name"]: self.parse_raw_image(raw_image)
            for raw_image in raw_images
        }
    
    def color_cycle(self, image_name: str):
        self.mutex.acquire()
        r, g, b = (255, 0, 0)
        image_mask = np.array(self.images[image_name])
        image_mask[image_mask > 0] = 1
        while self.color_cycle_run:
            r, g, b = next_color(r, g, b)
            image = image_mask * [r, g, b]
            self.set_pixels(image)

        self.clear()
        self.mutex.release()

    def intermittent_image(
            self,
            image_name: str,
            refresh_rate: float
        ):

        self.mutex.acquire()
        while self.intermittent_image_run:
            self.set_pixels(self.images[image_name])
            sleep(refresh_rate)
            self.clear()
            sleep(refresh_rate)

        self.mutex.release()

    def start_intermittent_image(
            self,
            image_name: str,
            refresh_rate: float
        ):

        self.intermittent_image_run = True
        thread = Thread(
            target=self.intermittent_image,
            args=(image_name, refresh_rate)
        )

        thread.start()

    def stop_intermittent_image(self):
        self.intermittent_image_run = False

    def start_color_cycle(self, image_mask: str):
        self.color_cycle_run = True
        thread = Thread(
            target=self.color_cycle,
            args=(image_mask, )
        )

        thread.start()

    def stop_color_cycle(self):
        self.color_cycle_run = False

    def set_image(self, image_name: str):
        self.mutex.acquire()
        self.set_pixels(self.images[image_name])
        self.mutex.release()
