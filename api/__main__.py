from . import create_app, db_connection

db = db_connection.connect()
app = create_app(db)
