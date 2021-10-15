# Demo Plan

## 1. Shell-in

docker run -d --name nginx nginx
docker exec -it nginx bash

docker run -d --name registry registry
docker exec -it registry bash
docker exec -it registry sh

docker run -d --name portainer portainer/portainer-ce
docker exec -it portainer bash
docker exec -it portainer sh
opener portainer
hostname
opener reg
hostname
opener nginx
hostname

## 2. Managing containers

**Open 3-terminals:**

- for docker
- for opener
- docker stats
**Run some containers:**

docker build app1 -t app1:v1.0
docker-compose up
**Show docker stats**

opener logs app
opener restart app
opener logs app
opener kill app
**Show docker stats**

opener kill demo
**Show docker stats**

## 3. Simple shell access

cp my-app/ my-lovely-app/ -R
cd my-lovely-app
docker-compose up -d
cd ..
rm my-lovely-app -rf

**new terminal!**
cd /
opener cdown lovely-app
