from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash , request
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
#forms
from forms import ChangePasswordForm, RegisterForm , LoginForm , ForgotPasswordForm
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
 #User DataBase
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    conformed_password: Mapped[str] = mapped_column(String(100), nullable=False)
with app.app_context():
    db.create_all()
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = (form.email.data or "").strip()
        password = (form.password.data or "").strip()
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password. Please try again.", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)

@app.route("/register" , methods = ["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = (form.email.data or "").strip()
        password = (form.password.data or "").strip()
        name = (form.name.data or "").strip()
        conformed_password = (form.conformed_password.data or "").strip()
        if(conformed_password!=password):
            flash("Conformed Password does'nt match the password" , "danger")
            return redirect(url_for("register"))
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists. Please log in instead.", "warning")
            return redirect(url_for("login"))
        if form.errors:
            flash("Please fill all the fields" , "danger")
            return redirect(url_for("register"))
        new_user = User(
          email=email,
          password=generate_password_hash(password, method='scrypt', salt_length=8),
          name=name,
          conformed_password=generate_password_hash(conformed_password, method='scrypt', salt_length=8)
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("login"))
    return render_template("register.html",form=form)
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))
@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    email = request.args.get("email")
    if not email:
        flash("Email is required to change password.", "danger")
        return redirect(url_for("login"))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        new_password = form.new_password.data.strip()
        confirm_password = form.confirm_password.data.strip()
        if new_password != confirm_password:
            flash("Passwords do not match. Please try again.", "danger")
            return redirect(url_for("change_password"))
        user = User.query.filter_by(email=email).first()
        if not user:
          flash("Email is not existed","danger")
          return redirect(url_for('Login'))
        if new_password == user.password:
            flash("New password should be different than the previous password","danger")
            return redirect(url_for('change_password'))
        user.password = generate_password_hash(new_password, method='scrypt', salt_length=8)
        db.session.commit()
        flash("Password changed successfully!", "success")
        return redirect(url_for("login"))
    return render_template("change_password.html", form=form)
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email not found. Please check and try again.", "danger")
            return redirect(url_for("forgot_password"))
        # Here you would typically send a password reset email with a token
        return redirect(url_for("change_password" , email=email))
    return render_template("verification_email.html", form=form)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
if __name__ == "__main__":
    app.run(debug=True)
