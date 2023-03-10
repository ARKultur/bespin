#!/usr/bin/env bash

set -eou pipefail

VENV_PATH=~/.local/venv_bespin

install_requirements () {
     [ -d "./venv" ] && { echo "Directory venv already exists. skipping requirements install" && return ; }

    echo "installing requirements"

    # Assumes you're using Ubuntu
    sudo apt install -y python3-pip 2>/dev/null || true

    python3 -m venv ${VENV_PATH} && \
    . ${VENV_PATH}/bin/activate && sudo -H pip3 install -r requirements.txt
}

install_postgresql () {
    # Assumes you're on Ubuntu for simplicity
    sudo apt-get install -y postgresql postgresql-contrib libpq-dev || true

    sudo systemctl start postgresql.service || true
    sudo /etc/init.d/postgresql start || true
    echo "setting up postgresql databases"

    export POSTGRES_USER="${USER}"
    export POSTGRES_PASSWORD="postgres"
    export POSTGRES_DB="bespin"

    # Create the database
    echo "Creating database $POSTGRES_DB"
    sudo -u postgres psql -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';" || true
    sudo -u postgres psql -c "GRANT postgres TO $POSTGRES_USER;" || true
    sudo -u postgres psql -c "CREATE DATABASE $POSTGRES_DB;"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;"
}


############
## SCRIPT ##
############

# install_requirements || exit 1

#. ${VENV_PATH}/bin/activate

install_postgresql
python3 manage.py migrate
