FROM python:3.5.2

RUN mkdir /app
RUN cd /app
COPY ./app .

ENTRYPOINT [ "python", "hydrator.py", "input-example.txt", "params-example.txt" ]