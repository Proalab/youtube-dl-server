# Youtube-dl Server created by [`Proalab`](proalab.com) 

**Original Images**

[`kmb32123/youtube-dl-server`](https://hub.docker.com/r/kmb32123/youtube-dl-server/) | 
[`manbearwiz/youtube-dl-server`](https://www.github.com/manbearwiz/youtube-dl-server)


Deployment
---

1. Push to Github account https://github.com/Proalab/youtube-dl-server
2. Build container localy with $ docker build -t proalab/youtube-dl-server:latest
3. Push container with $ docker push proalab/youtube-dl-server:latest
4. Push to Docker Hub will trigger automated CD Pipeline in Azure DevOps
5. CD Pipeline will execute command
```
 - az container create --resource-group Video-Downloader --name video-downloader --location westus --image proalab/youtube-dl-server --dns-name-label video-downloader --ports 80
```
6. This command rewrites Azure Container Instance and deploy a new version
7. After Update it might take up to 5 minutes for Azure Traffic Manager to redirect traffic to the new container

Azure Container Instance is being served through Traffic Manager which can be requested by custom domain and provides resilience and scalability


Docker Commands
---

```
docker build -t proalab/youtube-dl-server:latest --build-arg API_KEY='d<54a(2)tHLV[&jS' . ------ build container locally
docker images ------ all available images
docker ps -a ------ all running containers
docker run -t -p 80:80 proalab/youtube-dl-server ------ run whole container
docker run --rm=true -it youtube-dl-server /bin/bash ------ run console for container
docker run --rm=true -ti youtube-dl-server ls -l /usr/src/app ------ show files
docker exec -it youtube-dl-server bash ------ exec bash for running container

docker login
docker push proalab/youtube-dl-server:latest
```

**Clean Docker Containers and Docker Images**

```
docker stop $(docker ps -aq)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
```

Azure Container Instance
---

```
az container create --resource-group Video-Downloader --name video-downloader --location westus --image proalab/youtube-dl-server --dns-name-label video-downloader --ports 80
```

Heroku
---
```
heroku container:push web --app video-downloader-youtube-dl
heroku container:release web --app video-downloader-youtube-dl
```

Test with CURL
---

```
curl -X POST --data-urlencode "url=https://www.youtube.com/watch?v=Jm-k-RR1n7s" http://{URL}/youtube-dl
curl -X POST --data-urlencode "url=https://www.youtube.com/watch?v=Jm-k-RR1n7s" http://0.0.0.0/youtube-dl
```