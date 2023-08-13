name = Django Scrapper
DIR := $(abspath $(dir $(abspath $(lastword $(MAKEFILE_LIST))))..)
VENV = "$(DIR)/venv"

NO_COLOR=\033[0m	    # Color Reset
COLOR_OFF='\e[0m'       # Color Off
OK_COLOR=\033[32;01m	# Green Ok
ERROR_COLOR=\033[31;01m	# Error red
WARN_COLOR=\033[33;01m	# Warning yellow
RED='\e[1;31m'          # Red
GREEN='\e[1;32m'        # Green
YELLOW='\e[1;33m'       # Yellow
BLUE='\e[1;34m'         # Blue
PURPLE='\e[1;35m'       # Purple
CYAN='\e[1;36m'         # Cyan
WHITE='\e[1;37m'        # White
UCYAN='\e[4;36m'        # Cyan

all:
	@printf "Launch configuration ${name}...\n"
	@python manage.py runserver

app:
	@printf "Create new application...\n"
	@echo -e '$(WARN_COLOR)python ../manage.py startapp appname$(NO_COLOR)'

h:
	@printf "Django help\n"
	@python manage.py -h

help:
	@echo -e "$(OK_COLOR)==== All commands of ${name} configuration ====$(NO_COLOR)"
	@echo -e "$(WARN_COLOR)- app					: Create new application"
	@echo -e "$(WARN_COLOR)- make				        : Launch configuration"
	@echo -e "$(WARN_COLOR)- make h				: Django help"
	@echo -e "$(WARN_COLOR)- make make				: Make migrations"
	@echo -e "$(WARN_COLOR)- make makemigrations		        : Make makemigrations"
	@echo -e "$(WARN_COLOR)- make migrate			        : Make migrations"
	@echo -e "$(WARN_COLOR)- make req				: Install pip requirements"
	@echo -e "$(WARN_COLOR)- make root				: Create superuser"
	@echo -e "$(WARN_COLOR)- make venv				: Create virtual environment"
	@echo -e "$(WARN_COLOR)- make vexit				: Exit from virtual environment"
	@echo -e "$(WARN_COLOR)- make clean				: Remove venv configuration$(NO_COLOR)"

make:
	@printf "Launch configuration ${name}...\n"
	@python manage.py makemigrations

makemigrations:
	@printf "Make makemigrations ${name}...\n"
	@python manage.py makemigrations

migrate:
	@printf "Launch configuration ${name}...\n"
	@python manage.py migrate

venv:
	@printf "Launch virtual environment for ${name}...\n"
	@if [ ! -d "${VENV}" ]; then \
        echo "Creating virtual environment..."; \
        python3 -m venv ${VENV}; \
    fi
	@echo -e "$(OK_COLOR)Environment successfully created$(NO_COLOR)"
	@echo -e "$(WARN_COLOR)For activate use command:$(NO_COLOR)"
	@echo -e "$(OK_COLOR)source ../venv/bin/activate$(NO_COLOR)"

req:
	@printf "Install python requirements...\n"
	@if [ -d "${VENV}" ]; then \
		echo "Creating virtual environment..."; \
		pip install -r ../requirements.txt; \
	else \
		echo "Environment is absent"; \
		echo "In first run the command:"; \
		echo "make venv"; \
	fi

root:
	@printf "Create superuser for ${name}...\n"
	@python manage.py createsuperuser

vexit:
	@echo -e "$(WARN_COLOR)For deactivate environment $(NO_COLOR)"
	@echo -e "$(WARN_COLOR)use command:$(NO_COLOR)"
	@echo -e "$(OK_COLOR)deactivate$(NO_COLOR)"

clean:
	@printf "$(ERROR_COLOR)==== Cleaning configuration ${name}... ====$(NO_COLOR)\n"
	rm -rf ${VENV}

.PHONY	: all help make migrate venv vexit clean
