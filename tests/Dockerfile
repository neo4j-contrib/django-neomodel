FROM python:3
WORKDIR /usr/src/app
COPY .. .
RUN pip install -e '.[dev]'
RUN chmod +x ./tests/docker-entrypoint.sh
CMD ["./tests/docker-entrypoint.sh" ]
