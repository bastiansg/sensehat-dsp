include .env

.PHONY: core-build api-build devcontainer-build


core-build:
	[ -e .secrets/.env ] || touch .secrets/.env
	docker compose build sensehat-dsp-core

core-run:
	docker compose run sensehat-dsp-core


api-build: core-build
	docker compose build sensehat-dsp-api

api-run:
	docker compose up sensehat-dsp-api


devcontainer-build: core-build
	docker compose -f .devcontainer/docker-compose.yml build sensehat-dsp-devcontainer

devcontainer-run:
	docker compose -f .devcontainer/docker-compose.yml run sensehat-dsp-devcontainer
