FROM python:3
WORKDIR /usr/src/app
RUN pip install -e '.[dev]'
COPY .. .
RUN chmod +x ./tests/docker-entrypoint.sh
CMD ["./tests/docker-entrypoint.sh" ]
