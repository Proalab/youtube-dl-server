# Youtube-dl Server Based on another image

[`kmb32123/youtube-dl-server`](https://hub.docker.com/r/kmb32123/youtube-dl-server/) | 
[`manbearwiz/youtube-dl-server`](https://www.github.com/manbearwiz/youtube-dl-server)


Docker Commands

```
  $ docker build -t proalab/youtube-dl-server:latest --build-arg API_KEY='d<54a(2)tHLV[&jS' . ------ build container locally
  $ docker images ------ all available images
  $ docker ps -a ------ all running containers
  $ docker run -t -p 8080:8080 youtube-dl-server ------ run whole container
  $ docker run --rm=true -it youtube-dl-server /bin/bash ------ run console for container
  $ docker run --rm=true -ti youtube-dl-server ls -l /usr/src/app ------ show files
  $ docker exec -it youtube-dl-server bash ------ exec bash for running container

  $ docker login
  $ docker push proalab/youtube-dl-server:latest
```