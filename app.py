from db import db
from flask import Flask
from flask_cors import CORS
from routes.routes import blp


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

app.register_blueprint(blp)

# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    app.run(debug=True)