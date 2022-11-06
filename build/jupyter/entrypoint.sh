#!/bin/env sh

# reinstall local packages with no deps & edition mode
pip install --no-deps -e /src/sensehat_dsp

jupyter-lab --ip=0.0.0.0 --allow-root --no-browser
