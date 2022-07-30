#!/usr/bin/env bash

#python app/pre_start.py
#alembic upgrade head
uvicorn usgi:app --reload --host 0.0.0.0
