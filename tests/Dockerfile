FROM python:3
WORKDIR /usr/src/app
COPY ./tests/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY .. .
RUN chmod +x ./tests/docker-entrypoint.sh
CMD ["./tests/docker-entrypoint.sh" ]
