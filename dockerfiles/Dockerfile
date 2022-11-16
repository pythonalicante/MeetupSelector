FROM python:3.10


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt /tmp/requirements.txt
COPY requirements-dev.txt /tmp/requirements-dev.txt

RUN set -ex ;\
	apt-get update -y ; \
	apt-get install -y --no-install-recommends gettext ;\
	pip install --no-cache-dir -r /tmp/requirements-dev.txt ;\
	useradd -U app_user ;\
	install -d -m 0755 -o app_user -g app_user /app/static ;\
	rm -rf \
		/var/lib/apt/lists/*

WORKDIR /app
USER app_user:app_user

COPY --chown=app_user:app_user . .

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "server" ]
