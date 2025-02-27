from functools import lru_cache

from sensehat_dsp.display import Display


@lru_cache(maxsize=1)
def get_display() -> Display:
    return Display()
