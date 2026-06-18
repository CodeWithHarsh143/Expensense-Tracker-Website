from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user , login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
import os
from dotenv import load_dotenv
from datetime import date
load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("secret_key")
class Base(DeclarativeBase):
  pass

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
  "DBI_URI",
  "sqlite:///Expenses.db"
)
db = SQLAlchemy(model_class=Base)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
# User DataBase
class User(db.Model , UserMixin):
  __tablename__ = "users"
  
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
