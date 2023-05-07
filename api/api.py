from sensehat_dsp.display import Display

from fastapi import FastAPI
from sensehat_dsp.meta.data_models import Image, IntermittentImage


dsp = Display()
app = FastAPI()


@app.post("/set_image/")
async def set_image(image: Image):
    dsp.set_image(image)


@app.post("/intermittent_image/")
async def start_intermittent_image(intermittent_image: IntermittentImage):
    dsp.start_intermittent_image(intermittent_image)


@app.post("/color_cycle/")
async def start_color_cycle(image: Image):
    dsp.start_color_cycle(image)


@app.post("/reset/")
async def reset():
    dsp.reset()
