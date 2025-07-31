from flask import Flask
from models import db, init_db
from db_setup import initialize_database
from routes import main
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance/parking_app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

init_db(app)
app.register_blueprint(main)

if __name__ == '__main__':
    with app.app_context():
        initialize_database()  # ✅ Now runs only when main.py is directly run
    app.run(debug=True)

 

