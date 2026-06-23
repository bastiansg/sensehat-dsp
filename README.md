# sensehat-dsp

`sensehat_dsp` provides image and animation control for the Raspberry Pi Sense
HAT LED matrix.

## Used by P.O.R.

`sensehat_dsp` is a dependency of
[P.O.R. (Pop Oracle Robot)](https://github.com/bastiansg/por). It provides
P.O.R. with visual feedback for its state and activity through images and
animations on the Sense HAT display.

## Components

`Display` receives images or generated frames and writes them to the Sense HAT.
`Image`, `Color`, and `dsp_images` provide the content rendered by it.

```text
┌─────────────────────────────────────────────────────────────────────┐
│  SENSEHAT_DSP // DISPLAY PIPELINE                                  │
└─────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────┐
                    │     dsp_images      │
                    │   BUILT-IN ASSETS   │
                    └──────────┬──────────┘
                               │ Image
                               ▼
                    ┌─────────────────────┐
                    │       Display       │
                    │  EFFECT :: CONTROL  │
                    └──────────┬──────────┘
                               │ pixel matrix
                               ▼
                    ┌─────────────────────┐
                    │      Sense HAT      │
                    │    8 x 8 LED GRID   │
                    └─────────────────────┘
```

### [Display](src/sensehat_dsp/display/display.py)

`Display` is the interface between the library and the Sense HAT LED matrix.

### [Image and Color](src/sensehat_dsp/display/display.py)

`Image` and `Color` define the visual content handled by the display.

### [dsp_images](src/sensehat_dsp/display/dsp_images.py)

`dsp_images` is the library's collection of predefined visual assets.
