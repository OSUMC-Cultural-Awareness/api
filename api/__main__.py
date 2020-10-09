from . import db_connection, create_app

db = db_connection.connect()
app = create_app(db)
