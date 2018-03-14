sudo docker run -t -d --runtime=nvidia --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --device=/dev/video0 -v /home/tim/docker/detectron:/host prlcontainers.pxl.be/prl/detectron:0.1



sudo docker ps -a (kijk of hem up is + id)
sudo docker start <id>
sudo docker exec -it <container-id> /bin/bash
