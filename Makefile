help: ## Displays description of the goals - everything that is written after a double sharp (##) separated by a space
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

build-snapshot-tag: ## Build docker image with :snapshot tag
build-snapshot-tag:
	docker build dockerbuild -t artemkaxboy/opener:snapshot

publish-local-tag: ## Publish docker image with :local tag
publish-local-tag:
	docker build dockerbuild -t artemkaxboy/opener:local
	docker push artemkaxboy/opener:local
