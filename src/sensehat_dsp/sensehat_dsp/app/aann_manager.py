import numpy as np
import networkx as nx

from time import sleep

from typing import Callable
from threading import Thread, Lock

from sensehat_dsp.display import Display
from sensehat_dsp.logger import get_logger
from sensehat_dsp.display import dsp_images
from sensehat_dsp.meta.data_models import Image

from sensehat_dsp.pixoo_client import Pixoo
from sensehat_dsp.pixoo_client.image import cv2pil, scale_image


logger = get_logger(__name__)


def threaded(func: Callable):
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper


class AANNManager:
    def __init__(
        self,
        mac_address: str = "11:75:58:19:63:37",
        brightness: int = 100,
        wait_time: float = 3.0,
        max_wait_time: float = 4.0,
        min_wait_time: float = 0.1,
    ):
        self.dsp = Display()
        self.pixoo = Pixoo(mac_address=mac_address)

        self.brightness = brightness
        self.wait_time = wait_time
        self.max_wait_time = max_wait_time
        self.min_wait_time = min_wait_time

        self.pixoo.connect()
        self.pixoo.set_system_brightness(self.brightness)

        self.mutex = Lock()
        num_images = len(dsp_images)
        self.cycle_graph = nx.cycle_graph(
            num_images,
            create_using=nx.DiGraph,
        )

        self.reversed_cycle_graph = self.cycle_graph.reverse()
        self.max_graph_idx = num_images - 1
        self.cycle_graph_idx = self.max_graph_idx

        self.set_base_image(dsp_images[0])
        self.active_cycle = True
        self.start_cycle()

    def get_np_image(self, base_image: dict) -> np.ndarray:
        raw_image = [
            base_image["d-color"] if pix else base_image["l-color"]
            for pix in base_image["image"]
        ]

        np_image = np.array(raw_image).astype("uint8")
        np_image = np_image.reshape(8, 8, 3)

        return np_image

    def set_base_image(self, base_image: dict):
        self.dsp.set_image(Image(name=base_image["name"]))
        np_image = self.get_np_image(base_image)
        pil_image = cv2pil(scale_image(np_image, (16, 16)))
        self.pixoo.draw_pic(pil_image)

    def get_base_image(self, reversed: bool = False) -> dict:
        if reversed:
            idx = next(
                self.reversed_cycle_graph.neighbors(self.cycle_graph_idx)
            )

        else:
            idx = next(self.cycle_graph.neighbors(self.cycle_graph_idx))

        base_image = dsp_images[idx]
        self.cycle_graph_idx = idx

        return base_image

    @threaded
    def start_cycle(self):
        self.mutex.acquire()
        while self.active_cycle:
            self.set_base_image(self.get_base_image())
            sleep(self.wait_time)
            if self.cycle_graph_idx != self.max_graph_idx:
                continue

            for base_image in dsp_images:
                self.set_base_image(base_image)
                sleep(self.min_wait_time)

        self.mutex.release()

    def start(self):
        while True:
            event = self.dsp.stick.wait_for_event(emptybuffer=True)
            event_name = f"{event.action}_{event.direction}"
            # logger.info(event_name)
            if event_name == "released_middle":
                self.active_cycle = not self.active_cycle
                self.start_cycle()

            if event_name == "released_right":
                if self.active_cycle:
                    continue

                self.set_base_image(self.get_base_image())

            if event_name == "released_left":
                if self.active_cycle:
                    continue

                self.set_base_image(self.get_base_image(reversed=True))

            if event_name == "released_up":
                if not self.active_cycle:
                    continue

                inc_wait_time = self.wait_time + 0.5
                self.wait_time = min(self.max_wait_time, inc_wait_time)
                logger.info(f"wait_time => {self.wait_time}")

            if event_name == "released_down":
                if not self.active_cycle:
                    continue

                inc_wait_time = self.wait_time - 0.5
                self.wait_time = max(self.min_wait_time, inc_wait_time)
                logger.info(f"wait_time => {self.wait_time}")
