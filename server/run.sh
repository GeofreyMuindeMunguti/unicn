#!/usr/bin/env bash

#python app/pre_start.py
uvicorn usgi:app --reload --host 0.0.0.0
