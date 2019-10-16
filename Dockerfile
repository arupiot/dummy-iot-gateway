# dummy-gateway Dockerfile, primarily for serial_mon.py
# to be used in conjunction with mosquitto

FROM balenalib/raspberrypi3-debian:stretch

RUN [ "cross-build-start" ]

RUN apt-get update && apt-get upgrade

RUN apt-get install -y --no-install-recommends \
  apt-utils build-essential gcc make wget ntp ifmetric man iputils-ping

RUN apt-get -y install fbset\
    python3-dev python3-pip python3-pil python3-numpy python3-scipy

RUN apt-get clean

RUN mkdir /opt/code

COPY ./testing /opt/code

WORKDIR /opt/code/

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["serial_mon.py"]

RUN [ "cross-build-end" ]