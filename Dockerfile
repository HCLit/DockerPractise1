#FROM ubuntu:latest
#CMD ["echo", "Hello from my first docker file"]

FROM nginx:1.27.0

RUN apt-get update 
RUN apt-get install -y vim
