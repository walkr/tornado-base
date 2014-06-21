.PHONY: help

help:
	@echo
	@echo "USAGE: make [target]"
	@echo
	@echo "TARGETS:"
	@echo
	@echo "  install    - create virtual env, etc"
	@echo "    start    - start application"
	@echo "     test    - run tests"""
	@echo

install:
	@bash script/install.sh

start:
	@venv/bin/python app/server.py --logging=debug

test:
	@nosetests app/test --nologcapture

