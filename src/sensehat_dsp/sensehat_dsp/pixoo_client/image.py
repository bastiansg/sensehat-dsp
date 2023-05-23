import cv2

import numpy as np

from PIL import Image


def cv2pil(cv_image: np.ndarray) -> Image:
    # cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cv_image)

    return pil_image


def scale_image(
    cv_image: np.ndarray,
    resolution: tuple[int, int],
) -> np.ndarray:
    resized_image = cv2.resize(
        cv_image,
        resolution,
        interpolation=cv2.INTER_NEAREST,
    )

    return resized_image
