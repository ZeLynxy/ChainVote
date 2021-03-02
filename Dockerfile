FROM python:3.8


WORKDIR /chainvote-api

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install  --no-cache-dir  -r requirements.txt

VOLUME /chainvote-api 
ADD /chainvote-api  /chainvote-api

RUN wget https://github.com/trufflesuite/ganache/releases/download/v2.5.4/ganache-2.5.4-linux-x86_64.AppImage
RUN chmod +x ganache-2.5.4-linux-x86_64.AppImage
RUN ./ganache-2.5.4-linux-x86_64.AppImage --appimage-extract
RUN rm ganache-2.5.4-linux-x86_64.AppImage

ENV DISPLAY=host.docker.internal:0
EXPOSE 7545
ENTRYPOINT ["./squashfs-root/AppRun"]

#EXPOSE 8080


