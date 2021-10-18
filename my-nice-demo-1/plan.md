# Demo Plan

Для чего все это? **Фото.** Для работы с большими композ файлами, операции с контейнерами требуют либо входа в папку с docker-compose, либо указания полного имени с префиксами и постфиксам. Если запуск использовал несколько композ файлов или задавались переменные окружения, то задача по перезапуску, вообще, на грани фантастики.

Назначение инструмента

Цель доклада

## Setup

alias opener='docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener'

## 1. Shell-in

docker run -d --name nginx nginx
docker exec -it nginx bash

docker run -d --name registry registry
docker exec -it registry bash
docker exec -it registry sh

docker run -d --name demo-portainer portainer/portainer-ce
docker exec -it demo-portainer bash
docker exec -it demo-portainer sh
opener demo-portainer
hostname
exit

opener reg
hostname
exit

opener nginx
exit

## 2. Managing containers

**Open 3-terminals:**

- for docker
- for opener
- docker stats
**Run some containers:**

cd my-nice-demo-1
docker build app1 -t app1:v1.0
docker-compose up
**Show docker stats**

docker logs my-nice-demo-1_app1_1
opener logs app
opener restart app
opener logs app
opener kill app
**Show docker stats**

opener kill demo
**Show docker stats**

## 3. Upgrading images of running containers

docker pull netdata/netdata:v1.28.0
docker tag netdata/netdata:v1.28.0 netdata/netdata:latest

<!-- https://learn.netdata.cloud/docs/agent/packaging/docker#create-a-new-netdata-agent-container -->
docker run -d --name=netdata \
  -p 19999:19999 \
  -v netdataconfig:/etc/netdata \
  -v netdatalib:/var/lib/netdata \
  -v netdatacache:/var/cache/netdata \
  -v /etc/passwd:/host/etc/passwd:ro \
  -v /etc/group:/host/etc/group:ro \
  -v /proc:/host/proc:ro \
  -v /sys:/host/sys:ro \
  -v /etc/os-release:/host/etc/os-release:ro \
  --restart unless-stopped \
  --cap-add SYS_PTRACE \
  --security-opt apparmor=unconfined \
  netdata/netdata

<http://localhost:19999>

opener upgrade netd

<http://localhost:19999>

## 4. Managing compose

cp my-app/ my-lovely-app/ -R
cd my-lovely-app
docker-compose up -d
cd ..
rm my-lovely-app -rf

**new terminal!**
cd /
opener cdown lovely-app

## 5. Recreate

docker pull netdata/netdata:v1.28.0
docker tag netdata/netdata:v1.28.0 netdata/netdata:latest

opener recreate netdata

<http://localhost:19999>

## Clean

opener kill netdata
opener rm netdata
opener kill nginx
opener rm nginx
opener kill registry
opener rm registry
opener kill demo-portainer
opener rm demo-portainer
