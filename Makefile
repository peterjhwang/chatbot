include .env
export

install:
	pip install --upgrade pip pip-tools
	pip install wheel
	pip install -U -r requirements-dev.txt

requirements:
	pip-compile requirements.in -o requirements.txt --resolver=backtracking
	pip-compile requirements-dev.in -o requirements-dev.txt --resolver=backtracking