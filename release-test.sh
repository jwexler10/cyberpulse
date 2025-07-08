#!/usr/bin/env bash
set -e

# 1. Build & upload in your project venv
source venv/bin/activate
python -m pip install --upgrade build twine
rm -rf dist
python -m build
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="<TEST_PYPI_TOKEN>"
twine upload --repository testpypi dist/*
deactivate

# 2. Smoke-test install in a fresh env
python -m venv /tmp/cp-testenv
source /tmp/cp-testenv/bin/activate
pip install -i https://test.pypi.org/simple \
            --extra-index-url https://pypi.org/simple \
            cyberpulse==0.1.3
cyberpulse --help
