from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
from flask_mail import Mail

app = Flask(__name__)

app.config.from_object('config.Config')

app.permanent_session_lifetime = timedelta(minutes=30)

app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USERNAME'] = 'f4d5b610e9d791'
app.config['MAIL_PASSWORD'] = 'ced7d842e9d271'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


import routes
from models import Position, Order, User


if __name__ == '__main__':
    app.run(debug=True)
