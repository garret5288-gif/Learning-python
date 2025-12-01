from flask import Flask, request, render_template_string, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy

DB_PATH = os.path.join(os.path.dirname(__file__), "community_forum.db")

db = SQLAlchemy()

