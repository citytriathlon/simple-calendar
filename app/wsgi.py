"""Gunicorn entrypoint: `gunicorn wsgi:app`."""

from app import app, start_updater

start_updater()

__all__ = ["app"]
