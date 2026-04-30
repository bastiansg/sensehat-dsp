from threading import Thread
from typing import TypeVar, Callable, Any


F = TypeVar("F", bound=Callable[..., None])


def threaded(func: Callable[..., None]) -> Callable[..., None]:
    def wrapper(*args: Any, **kwargs: Any) -> None:
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    return wrapper


def next_color(r: int, g: int, b: int) -> tuple[int, int, int]:
    if r == 255 and g < 255 and b == 0:
        g += 1

    if g == 255 and r > 0 and b == 0:
        r -= 1

    if g == 255 and b < 255 and r == 0:
        b += 1

    if b == 255 and g > 0 and r == 0:
        g -= 1

    if b == 255 and r < 255 and g == 0:
        r += 1

    if r == 255 and b > 0 and g == 0:
        b -= 1

    return r, g, b
