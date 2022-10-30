SHELL=/bin/bash
DOCKER_COMPOSE=docker compose
DOCKER_ENVIRONMENT=docker-compose.yml
PRE_RUN_API_COMMAND=${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} run --rm django
PACKAGE_NAME=meetupselector
VENV_FOLDER=venv
LAUNCH_IN_VENV=source ${VENV_FOLDER}/bin/activate &&
PYTHON_VERSION=python3.10

# target: all - Default target. Does nothing.
all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: setup - prepare environment
setup:
	rm -rf ${VENV_FOLDER}
	${PYTHON_VERSION} -m venv ${VENV_FOLDER}
	${LAUNCH_IN_VENV} pip install -r requirements-dev.txt

# target: setup-docs - install the requirements to launch the docs locally
setup-docs: setup
	${LAUNCH_IN_VENV} pip install -r requirements-doc.txt

.PHONY: docs
# target: docs - launch the mkdocs server
docs:
	${LAUNCH_IN_VENV} mkdocs serve

# target: build - Build the docker images
build:
	${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} build

# target: run - Run the project
run:
	${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} up -d

# taget: down - Stop the project
down:
	${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} down

# target: clean-volumes - Stop the project and clean all volumes
clean-volumes:
	${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} down -v

# target: logs - Show project logs
logs:
	${DOCKER_COMPOSE} -f ${DOCKER_ENVIRONMENT} logs -f

# target: createsuperuser - Create a superuser for django-admin
createsuperuser:
	${PRE_RUN_API_COMMAND} createsuperuser

# target: test - test code
.PHONY: test
test:
	${PRE_RUN_API_COMMAND} test

# target: bash - bash code
.PHONY: bash
bash:
	${PRE_RUN_API_COMMAND} bash

# target: lint - Lint the code
.PHONY: lint
lint:
	${PRE_RUN_API_COMMAND} lint

# target: shell - Obtain a django shell
.PHONY: shell
shell:
	${PRE_RUN_API_COMMAND} shell

# target: makemigrations - Create the migrations of the database
.PHONY: makemigrations
makemigrations:
	${PRE_RUN_API_COMMAND} makemigrations

# target: apply_black_isort - Run black and isort
apply_black_isort:
	${LAUNCH_IN_VENV} black ${PACKAGE_NAME} tests
	${LAUNCH_IN_VENV} isort ${PACKAGE_NAME} tests
