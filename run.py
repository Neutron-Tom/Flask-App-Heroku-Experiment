from app import app
from db import db

db.init_app(app)

# Get SQLAlchemy to build tables in data.db for us
@app.before_first_request
def create_tables():
    db.create_all()
