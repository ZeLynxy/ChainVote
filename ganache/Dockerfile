 FROM debian:stable-slim
RUN apt-get update
RUN apt-get install -y wget fuse libgtk-3-dev libgtkextra-dev libgconf2-dev libnss3 libasound2 libxtst-dev libxss1 libx11-6 libx11-xcb-dev
RUN wget https://github.com/trufflesuite/ganache/releases/download/v2.5.4/ganache-2.5.4-linux-x86_64.AppImage
RUN chmod +x ganache-2.5.4-linux-x86_64.AppImage

RUN ./ganache-2.5.4-linux-x86_64.AppImage --appimage-extract
#RUN sed -i 's/exec "$BIN"/exec "$BIN" --no-sandbox/g' ./squashfs-root/AppRun

#RUN ./ganache-2.5.4-linux-x86_64.AppImage --appimage-extract
#RUN ./appimagetool-x86_64.AppImage -n --comp xz ./squashfs-root ganache-2.5.4-linux-x86_64.AppImage

#RUN rm ganache-2.5.4-linux-x86_64.AppImage

#RUN ls ./squashfs-root 
#RUN  cat ./squashfs-root/AppRun
RUN apt-get install -y libcanberra-gtk-module libcanberra-gtk3-module


WORKDIR "/squashfs-root"
RUN ls

#ENV DISPLAY=:0
EXPOSE 7545
RUN VIDEO_CARDS="intel i965" 
#add path 'dri/*' mode 0666 group video
#add path 'dri/*' mode 0666 group video


CMD ./AppRun

#ENTRYPOINT ["./squashfs-root/AppRun"]
