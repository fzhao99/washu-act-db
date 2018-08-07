# !/usr/bin/env bash
# File path should be ./bin/post_compile
# (.sh extension added in Gist just to enable shell syntax highlighting.

echo "=> Performing database migrations..."
python manage.py migrate
