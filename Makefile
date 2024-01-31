.PHONY: all

all: remove build run

rerun: stop remove build run

detached: remove build run-d

build:
	@docker compose build

run:
	@docker compose up --remove-orphans

run-d:
	@docker compose up -d --remvove-orphans

remove:
	@docker compose down
	@docker compose rm

stop:
	@docker compose down