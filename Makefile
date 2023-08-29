ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

# parse additional args for commands

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

APPLICATION_NAME = app
TEST = poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG
CODE = $(APPLICATION_NAME) tests

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \


# Commands
env:  ##@Environment Create .env file with variables for localhost use
	@$(eval SHELL:=/bin/bash)
	@cp .env.example .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env

env_prod:  ##@Environment Create .env file with variables for docker
	@$(eval SHELL:=/bin/bash)
	@cp .env.example.docker .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

db:  ##@Database Create database with docker-compose
	docker-compose -f docker-compose.yml up -d --remove-orphans

lint:  ##@Code Check code with pylint
	poetry run python3 -m pylint $(CODE)

format:  ##@Code Reformat code with isort and black
	poetry run python3 -m isort $(CODE)
	poetry run python3 -m black $(CODE)

format_w:  ##@Code Reformat code with isort and black on windows
	poetry run python -m isort $(CODE)
	poetry run python -m black $(CODE)

migrate:  ##@Database Do all migrations in database
	alembic upgrade $(args)

run:  ##@Application Run application server
	poetry run python3 -m $(APPLICATION_NAME)

run_w:  ##@Application Run application server on windows
	poetry run python -m $(APPLICATION_NAME)

run_prod:
	python3 -m $(APPLICATION_NAME)

revision:  ##@Database Create new revision file automatically with prefix (ex. 2022_01_01_14cs34f_message.py)
ifdef title
	alembic revision --autogenerate -m "$(title)"
else
	alembic revision --autogenerate
endif

test:  ##@Testing Test application with pytest
	$(TEST)

test-cov:  ##@Testing Test application with pytest and create coverage report
	$(TEST) --cov=$(APPLICATION_NAME) --cov-report html --cov-fail-under=70

clean:  ##@Code Clean directory from garbage files
	rm -fr *.egg-info dist

%::
	echo $(MESSAGE)
