from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash , request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user , login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey , Float,Date
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from calendar import month_name
import os
from dotenv import load_dotenv
from datetime import date
#forms
from forms import ChangePasswordForm, RegisterForm , LoginForm , ForgotPasswordForm,AddExpenseForm,ReportForm
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
    user_expenses = relationship(
        "Expenses",
      back_populates="user"
    )
class Expenses(db.Model,UserMixin):
  __tablename__ = "expenses"
  id:Mapped[int] = mapped_column(Integer,primary_key=True)
  amount:Mapped[float] = mapped_column(Float,nullable=False)
  expense_title:Mapped[str] = mapped_column(String(100),nullable=False)
  category:Mapped[str] = mapped_column(String(100),nullable=False)
  date_feild:Mapped[date] = mapped_column(Date,nullable=False)
  note:Mapped[str] = mapped_column(String(200),nullable=True)
  user_id:Mapped[int] =mapped_column(
    ForeignKey("users.id"),
    nullable=False
  )
  user = relationship(
    "User",
    back_populates="user_expenses",
  )

with app.app_context():
    db.create_all()
@app.route("/")
def home():
    if(not current_user.is_authenticated):
        flash("You need to login first to view your dashboard","info")
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
        new_password = (form.new_password.data or "").strip()
        confirm_password =( form.confirm_password.data or "").strip()
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
        email = (form.email.data or "").strip()
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email not found. Please check and try again.", "danger")
            return redirect(url_for("forgot_password"))
        # Here you would typically send a password reset email with a token
        return redirect(url_for("change_password" , email=email))
    return render_template("verification_email.html", form=form)
@app.route("/add_expenses",methods = ["GET","POST"])
def add_expense():
  if(not current_user.is_authenticated):
    flash("You need to login first to add expenses","danger")
    return redirect(url_for("login"))
  form = AddExpenseForm()
  if form.validate_on_submit():
    expense_title = (form.expense_title.data or "").strip()
    amount = form.amount.data
    Date = form.date.data
    print(Date)
    categ = form.category.data
    note = form.note.data
    expense = Expenses(
      amount = amount,
      expense_title = expense_title,
      category = categ,
      date_feild = Date,
      note = note,
      user = current_user
    )
    db.session.add(expense)
    db.session.commit()
    return redirect(url_for('expense_analysis'))
  else:
    print(form.errors)
    print(request.form)
  return render_template('add_expenses.html',form= form)
@app.route("/Reports",methods=["GET", "POST"])
def reports():
  if(not current_user.is_authenticated):
        flash("You need to login first to view your expenses","danger")
        return redirect(url_for("login"))
  form = ReportForm()
  show_chards = False
  show_cards = False
  total_expense = 0
  highest_category = ""
  transaction_count = 0
  category_data = {}
  monthly_data = {
    "labels":[],
    "values":[]
  }
  try:
    if form.validate_on_submit():
      start_date = form.start_date.data
      end_date = form.end_date.data

      if(start_date and end_date):
        show_chards = True
        show_cards = True
      # needs: 1.total expense
      #       2.highest category
      #       3.total transaction_count
      #       4.e.g for pie chart
      #       category_data = {
      #       "Food": 5000,
      #       "Travel": 3000,
      #       "Shopping": 2000
      #       }
      #       5. for bar chart eg.
      #       month to expenses
      #       const monthlyData = {
      #           labels:["Jan","Feb","Mar"],
      #           values:[1000,2000,3000]
      #       };
      max_cnt = 0
      if start_date>date.today() or end_date>date.today():
        flash("Dates cannot be in the future.", "danger")
        return redirect(url_for("reports"))
      if not start_date or not end_date:
        flash("Please select both start and end dates.", "danger")
        return redirect(url_for("reports"))
      if start_date > end_date:
        flash("Start date cannot be after end date.", "danger")
        return redirect(url_for("reports"))
      show_chards = True
      show_cards = True
      expenses = Expenses.query.filter(
        Expenses.user_id == current_user.id,
        Expenses.date_feild.between(start_date, end_date)
      ).order_by(Expenses.date_feild.asc()).all()
      if not expenses:
        flash("No expenses found in the selected date range.", "info")
        return redirect(url_for("reports"))
      transaction_count = len(expenses)
      category_data = {}
      monthly_expense = {}
      for expense in expenses:
        total_expense += expense.amount
        if(expense.category in category_data):
          category_data[expense.category]+=1
        else:
          category_data[expense.category]=1
        if(max_cnt<category_data[expense.category]):
          highest_category = expense.category
          max_cnt = category_data[expense.category]
        if(expense.date_feild.month in monthly_expense):
           monthly_expense[expense.date_feild.month]+=expense.amount
        else:
          monthly_expense[expense.date_feild.month] = expense.amount

      monthly_data = {
        "labels":[],
        "values":[]
      }
      for key,val in monthly_expense.items():
        monthly_data["labels"].append(month_name[key])
        monthly_data["values"].append(val)
  except Exception as e:
    print(e)
  return render_template("reports.html",form = form,total_expense=total_expense,highest_category=highest_category,transaction_count=transaction_count,category_data=category_data,monthly_data=monthly_data,show_chards=show_chards,show_cards=show_cards)
@app.route("/expense_analysis")
def expense_analysis():
    if(not current_user.is_authenticated):
        flash("You need to login first to view your expenses","danger")
        return redirect(url_for("login"))
    expenses = current_user.user_expenses
    return render_template("expenses.html", expenses=expenses)
@app.route("/edit_expense",methods=["GET","POST"])
def edit_expense():
  expense_id = request.args.get("id")
  expense = Expenses.query.get(expense_id)
  form = AddExpenseForm(obj=expense)
  if request.method == "GET": # manually changing date format for autofill when form is not submitted (means at get not post)
    form.date.data = Date(
      expense.year,
      expense.month,
      expense.day

   )
  if not expense:
    flash("Expense not found.", "danger")
    return redirect(url_for("expense_analysis"))
  if expense.user_id != current_user.id:
    flash("You are not authorized to edit this expense.", "danger")
    return redirect(url_for("expense_analysis"))
  # Here you would typically render an edit form and handle the update logic
  if form.validate_on_submit():
    expense.amount = form.amount.data
    expense.note = (form.note.data or "").strip()
    expense.expense_title = (form.expense_title.data or "").strip()
    expense.category = form.category.data
    date = form.date.data
    expense.day = date.day
    expense.month = date.month
    expense.year = date.year
    db.session.commit()
    flash("Expense updated successfully!", "success")
    return redirect(url_for("expense_analysis"))
  return render_template("add_expenses.html",form=form,is_edit=True) # we can use the same form using is_edit flag to differentiate between add and edit forms
@app.route("/delete_expense")
def delete_expense():
  expense_id = request.args.get("id")
  expense = Expenses.query.get(expense_id)
  if not expense:
    flash("Expense not found.", "danger")
    return redirect(url_for("expense_analysis"))
  if expense.user_id != current_user.id:
    flash("You are not authorized to delete this expense.", "danger")
    return redirect(url_for("expense_analysis"))
  db.session.delete(expense)
  db.session.commit()
  flash("Expense deleted successfully!", "success")
  return redirect(url_for("expense_analysis"))

@app.route("/dashboard")
def dashboard():
    if(not current_user.is_authenticated):
        flash("You need to login first to view your dashboard","danger")
        return redirect(url_for("login"))
    expenses = current_user.user_expenses
    return render_template("dashboard.html", expenses=expenses)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
if __name__ == "__main__":
    app.run(debug=True)
