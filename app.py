from db import db
from flask import Flask
from flask_cors import CORS
from routes.routes import blp
from models.init_models import insert_initial_data


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

app.register_blueprint(blp)

with app.app_context():
    db.create_all()
    insert_initial_data()

if __name__ == '__main__':
    app.run(debug=True)