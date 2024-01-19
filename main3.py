from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))


class RegForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Зарегистрироваться')


@app.route('/', methods=['GET', 'POST'])
def base():
    form = RegForm()
    users = User.query.all()
    if form.validate_on_submit():
        security_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                        password=security_password)

        db.session.add(new_user)
        db.session.commit()
        users = User.query.all()

        form.first_name.data = ''
        form.last_name.data = ''
        form.email.data = ''
        form.password.data = ''

    return render_template('base.html', form=form, users=users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
