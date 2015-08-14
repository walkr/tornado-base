.PHONY: help

help:
	@echo
	@echo "USAGE: make [target]"
	@echo
	@echo "TARGETS:"
	@echo
	@echo "local.app.start                      - start app"
	@echo "local.app.test                       - run tests"
	@echo "local.app.deps.get                   - get deps"
	@echo "local.app.install                    - create virtualenv, etc"
	@echo
	@echo "local.sql.init                       - init database (create tables, etc)"
	@echo "local.sql.backup                     - backup database"
	@echo "local.sql.restore                    - restore database"
	@echo
	@echo "remote.app.push                      - push app code to remote machines"
	@echo "remote.app.install                   - install app on remote machines"
	@echo "remote.app.start                     - start app on remote machines"
	@echo "remote.app.stop                      - stop app on remote machines"
	@echo "remote.app.restart                   - restart app on remote machines"
	@echo
	@echo "remote.sql.init                      - remote init database (create tables, etc)"
	@echo "remote.sql.backup                    - remote backup database"
	@echo "remote.sql.restore                   - remote restore database"
	@echo
	@echo "remote.machine.upgrade               - upgrade remote machines"
	@echo "remote.machine.do c=<command>        - execute <command>"
	@echo "remote.machine.sudo.do c=<command>   - execute <command> w/ sudo"
	@echo
	@echo "FABRIC USAGE:"
	@echo
	@echo "fab help                             - lists tasks"
	@echo "fab -P --roles [app|prx] task_name   - execute 'task_name' in parallel"
	@echo


# =========================
# LOCAL TASKS
# =========================

local.app.install:
	@bash script/app.install.sh

local.app.start:
	@venv/bin/python app/server.py --logging=debug

local.app.test:
	@venv/bin/nosetests app/test --nologcapture

local.app.deps.get:
	@bash script/app.deps.get.sh

local.sql.init:
	@venv/bin/python script/sql.init.py

local.sql.backup:
	@bash script/sql.backup.sh

local.sql.restore:
	@bash script/sql.restore.sh


# =========================
# REMOTE TASKS
# =========================

remote.app.push:
	@fab -P --roles app remote_app_push

remote.app.install:
	@fab -P --roles app remote_app_install

remote.app.start:
	@fab -P --roles app remote_app_start

remote.app.stop:
	@fab -P --roles app remote_app_stop

remote.app.restart:
	@fab -P --roles app remote_app_restart

remote.app.test:
	@fab -P --roles app remote_app_test



local.sql.init:
	@fab -P --roles sql remote_sql_init

local.sql.backup:
	@fab -P --roles sql remote_sql_backup

local.sql.restore:
	@fab -P --roles sql remote_sql_restore



remote.machine.upgrade:
	@fab -P --roles all remote_machine_upgrade

remote.machine.do:
	@fab -P --roles all remote_machine_do:$(c)

remote.machine.sudo.do:
	@fab -P --roles all remote_machine_sudo_do:$(c)
