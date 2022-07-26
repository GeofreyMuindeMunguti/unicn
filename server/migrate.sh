#!/usr/bin/env bash

export $(grep -v '^#' .env.local | xargs)

export PYTHONPATH=.

alembic upgrade head
