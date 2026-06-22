from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , EmailField , PasswordField,IntegerField,FloatField,DateField,SelectField,TextAreaField
from wtforms.validators import DataRequired, URL , Email, EqualTo, Length

class RegisterForm(FlaskForm):
    email = EmailField("Email",render_kw={"placeholder": "Email" , "class": "w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500"}, validators=[DataRequired(), Email()])
    password = PasswordField("Password",render_kw={"placeholder": "Password" , "class": "w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500"}, validators=[DataRequired()])
    name = StringField("Name",render_kw={"placeholder": "Full Name" , "class": "w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500"}, validators=[DataRequired()])
    conformed_password = PasswordField("Confirm Password",render_kw={"placeholder": "Confirm Password" , "class": "w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500"}, validators=[DataRequired()])
    submit = SubmitField("Create Account", render_kw={"class": "w-full bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-3 px-4 rounded-xl focus:outline-none focus:shadow-outline"})
class LoginForm(FlaskForm):
    email = EmailField("Email",render_kw={"placeholder": "Email" , "class": "w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500"}, validators=[DataRequired(), Email()])
    password = PasswordField("Password",render_kw={"placeholder": "Password" , "class": "w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500"}, validators=[DataRequired()])
    submit = SubmitField("Login", render_kw={"class": "w-full bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-semibold py-3 rounded-xl transition"})
class ChangePasswordForm(FlaskForm):
    new_password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(min=8)],
        render_kw={
            "placeholder": "New Password",
            "class": "w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500"
        }
    )

    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("new_password", message="Passwords must match")
        ],
        render_kw={
            "placeholder": "Confirm New Password",
            "class": "w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500"
        }
    )
    submit = SubmitField(
        "Change Password",
        render_kw={
            "class": "w-full bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-3 px-4 rounded-xl focus:outline-none focus:shadow-outline"
        }
    )

class ForgotPasswordForm(FlaskForm):

    email = StringField(
        validators=[
            DataRequired(),
            Email()
        ],
        render_kw={
            "placeholder": "Email Address",
            "class": "w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500"
        }
    )
    submit = SubmitField(
        "Check Email",
        render_kw={
            "class": "w-full bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-3 px-4 rounded-xl focus:outline-none focus:shadow-outline"
        }
    )

class AddExpenseForm(FlaskForm):
  expense_title = StringField(validators=[DataRequired()],render_kw={
    "placeholder":"e.g Pizza,Uber Ride",
    "class":"w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white focus:outline-none focus:border-emerald-500"
  })

  amount = FloatField(validators=[DataRequired()],render_kw={
    "placeholder":"0.00",
    "class":"w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white focus:outline-none focus:border-emerald-500"
  })

  date = DateField(validators=[DataRequired()],format="%Y-%m-%d",render_kw={
    "class":"w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white focus:outline-none focus:border-emerald-500"
  })

  category = SelectField(
    choices=[
        # (value , label)
        ("food", "Food"),
        ("transport", "Transport"),
        ("shopping", "Shopping"),
        ("entertainment", "Entertainment"),
        ("bill","Bills"),
        ("healthcare","HealthCare"),
        ("other","Other")
    ],
    render_kw={
      "class":"w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white focus:outline-none focus:border-emerald-500",
    }
  )
  note = TextAreaField(
  render_kw={
    "class":"w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white focus:outline-none focus:border-emerald-500",
    "placeholder":"Optional Notes"
  }
  )
  submit = SubmitField(
  "Save Expense",
  render_kw={
    "class":"px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-black font-semibold rounded-lg transition"
  }
  )







