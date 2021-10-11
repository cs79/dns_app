FROM python:3.8

RUN apt-get update \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN groupadd -g 799 nyu && \
    useradd -r -u 999 -g nyu nyu

# Set up a working folder and install the pre-reqs
WORKDIR /app

RUN pip install pandas flask_api

VOLUME [ "/db" ]

USER nyu

COPY --chown=nyu:nyu . .

# change to root to avoid access issues with file in volume (not safe in real app, obviously)
USER root

CMD [ "python", "./dns_server.py" ]