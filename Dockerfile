FROM debian:buster
COPY alarm_capture.py requirements.txt ./
RUN apt-get update && apt-get upgrade -y
RUN apt install python3-opencv python3-pip -y
RUN pip3 install -r requirements.txt

CMD ["python3","./alarm_capture.py"]




