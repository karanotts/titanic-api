APP_NAME = "Titanic API"
PYTHON = python3.9

.PHONY: install test

default: run

install:
	${PYTHON} -m venv env ; \
	. ../env/bin/activate ; \
	pip install -r requirements.txt

db:
	docker run --name titanic_db -d -p 27017:27017 mongo:latest ; \
	mongoimport --type csv -d titanic -c people --headerline --drop data/titanic.csv

test:
	. ../env/bin/activate ; \
	PYTHONPATH=./src/app pytest --verbose

run:
	. ../env/bin/activate ; \
	PYTHONPATH=./src/app uvicorn main:api --host 0.0.0.0 --port 8000 --reload

clean:
	docker stop titanic_db ; \
	docker rm titanic_db ; \
	rm -rf env
