from sensehat_dsp.display import Display

from fastapi import FastAPI
from models import Image, IntermittentImage


dsp = Display()
app = FastAPI()


@app.post('/set_image/')
async def generate(image: Image):
    dsp.stop_all()
    dsp.set_image(image.image_name)
    return

@app.post('/intermittent_image/')
async def generate(intermittent_image: IntermittentImage):
    dsp.stop_all()
    dsp.start_intermittent_image(
        intermittent_image.image_name,
        intermittent_image.refresh_rate
    )

    return

@app.post('/color_cycle/')
async def generate(image: Image):
    dsp.stop_all()
    dsp.start_color_cycle(image.image_name)
    return
