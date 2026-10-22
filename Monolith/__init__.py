"""
Run:   flask --app asma run
Data:  ./data/asma.db, created on first start together with the operator
       account "admin", whose temporary password is printed to the console once.
"""
import os
import secrets
from datetime import timedelta
from pathlib import Path

from flask import Flask

from . import db


def create_app():
    app = Flask(__name__)
    app.config.update(
        # Signs the session cookie. Without ASMA_SECRET_KEY a random key is
        # generated, so everyone is signed out when the application restarts.
        SECRET_KEY=os.environ.get("ASMA_SECRET_KEY") or secrets.token_hex(32),
        DATABASE=Path(os.environ.get("ASMA_DATA_DIR", "data")) / "asma.db",
        # Largest network target, in addresses.
        MAX_NETWORK_ADDRESSES=1024,
        # A session ends after 30 minutes without a request. Flask re-signs the
        # cookie on every request and rejects cookies older than this.
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    db.init_app(app)

    return app
