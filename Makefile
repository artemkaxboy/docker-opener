.DEFAULT_GOAL := help
DOCKER_REGISTRY_USERNAME = artemkaxboy
version = snapshot
now = $(shell date)

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

build: ## Build docker images with :snapshot tag
build:
	docker buildx build -t ${DOCKER_REGISTRY_USERNAME}/opener:${version} --build-arg CREATED="${now}" dockerbuild
