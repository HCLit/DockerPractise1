#FROM ubuntu:latest
#CMD ["echo", "Hello from my first docker file"]

FROM nginx:1.27.0
CMD apt-get update && apt-get install -y vim
