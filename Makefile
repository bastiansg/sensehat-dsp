.PHONY: core-build api-build devcontainer-build


core-build:
	docker compose build sensehat-dsp-core

core-run:
	docker compose run sensehat-dsp-core


api-build: core-build
	docker compose build sensehat-dsp-api

api-run: api-build
	docker compose run --rm sensehat-dsp-api

api-up: api-build
	docker compose up sensehat-dsp-api -d


devcontainer-build: core-build
	docker compose -f .devcontainer/docker-compose.yml build sensehat-dsp-devcontainer
