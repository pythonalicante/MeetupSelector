SHELL=/bin/bash
DOCKER_COMPOSE=docker-compose
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

# target: lint - Lint the code
.PHONY: lint
lint:
	${PRE_RUN_API_COMMAND} lint
