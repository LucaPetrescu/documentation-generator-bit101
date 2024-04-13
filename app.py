from db import db
from flask import Flask
from flask_cors import CORS
from routes.routes import blp
import os


app = Flask(__name__, instance_path=os.path.join(os.path.expanduser('~'), 'documentation-generator'))
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

app.register_blueprint(blp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print(os.environ['FLASK_RUN_PORT'])
    app.run(debug=True, host=0.0.0.0, port=8000)