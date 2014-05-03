all:
	help

help:
	@echo
	@echo "USAGE: make [target]"
	@echo
	@echo "TARGETS:"
	@echo
	@echo "  install            - run installation routines"
	@echo "  start-dev       	- start app in dev mode (w/ logging)"
	@echo "  start-prod       	- start app in prod mode (less logging)""
	@echo "  test           	- run tests"""

install:
	@bash script/install.sh

start-prod:
	@venv/bin/python app/server.py --logging=error

start-dev:
	@venv/bin/python app/server.py --logging=debug

test:
	@nosetests app/test --nologcapture

