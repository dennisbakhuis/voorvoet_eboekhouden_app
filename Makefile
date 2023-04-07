help: ## Show this help
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-pre-commit: ## Install pre-commit hooks
	pre-commit install

test: ## Run pytest and report coverage
	pytest --cov-report term-missing --cov=voorvoet_app

requirements: ## create requirements.txt
	poetry export --without-hashes --format=requirements.txt > requirements.txt

docker: ## Build docker image
	poetry export --without-hashes --format=requirements.txt > requirements.txt
	docker build --platform=linux/amd64 -t voorvoet_eboekhouden_app .
	docker tag voorvoet_eboekhouden_app dennisbakhuis/voorvoet_eboekhouden_app
	docker push dennisbakhuis/voorvoet_eboekhouden_app

docker-local: ## Build docker image only locally
	poetry export --without-hashes --format=requirements.txt > requirements.txt
	docker build --platform=linux/amd64 -t voorvoet_eboekhouden_app .

.PHONY: help init test
