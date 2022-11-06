core-build:
	docker compose build sensehat-dsp-core

core-run:
	docker compose run sensehat-dsp-core


jupyter-build: core-build
	docker compose build sensehat-dsp-jupyter

jupyter-run:
	docker compose up sensehat-dsp-jupyter
