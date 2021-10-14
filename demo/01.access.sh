docker-compose up -d
opener logs web --follow
# Ctrl+C
opener logs db --follow --tail 3
# Ctrl+C
docker-compose down
