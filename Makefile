.PHONY: help

help:
	@echo
	@echo "USAGE: make [target]"
	@echo
	@echo "TARGETS:"
	@echo
	@echo " app.install   - create virtual env, etc"
	@echo " app.start     - start application"
	@echo " app.test      - test application"
	@echo
	@echo " deps.get      - download dependencies"
	@echo

app.install:
	@bash script/app.install.sh

app.start:
	@venv/bin/python app/server.py --logging=debug

app.test:
	@nosetests app/test --nologcapture

deps.get:
	@bash script/deps.get.sh