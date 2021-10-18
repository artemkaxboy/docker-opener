# Plan

## 3. Upgrading images of running containers

docker pull netdata/netdata:v1.28.0
docker tag netdata/netdata:v1.28.0 netdata/netdata:latest

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

## 5. Recreate

docker pull netdata/netdata:v1.28.0
docker tag netdata/netdata:v1.28.0 netdata/netdata:latest

opener recreate netdata

<http://localhost:19999>
