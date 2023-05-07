import sys

from sensehat_dsp.display import Display

# from sensehat_dsp.pixoo_client import Pixoo

from sensehat_dsp.logger import get_logger


logger = get_logger(__name__)


def main():
    dsp = Display()
    # pixoo = Pixoo(mac_address="11:75:58:19:63:37")
    # pixoo.connect()
    while True:
        event = dsp.stick.wait_for_event(emptybuffer=True)
        logger.info(f"{event.action}_{event.direction}")


if __name__ == "__main__":
    sys.exit(main())
