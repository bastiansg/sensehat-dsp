import sys

from sensehat_dsp.logger import get_logger
from .aann_manager import AANNManager


logger = get_logger(__name__)


def main():
    aann_manager = AANNManager()
    aann_manager.start()


if __name__ == "__main__":
    sys.exit(main())
