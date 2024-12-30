import sqlalchemy as db
from db_credentials import *  # create db_credentials.py with variable: DATABASE_URI = 'your/database/uri' inside.

engine = db.create_engine(DATABASE_URI)
conn = engine.connect()

metadata = db.MetaData()
User = db.Table('Users', metadata, autoload_with=engine)
Shop = db.Table('Shops', metadata, autoload_with=engine)
Product = db.Table('Products', metadata, autoload_with=engine)
Scan_history = db.Table('Scan_history', metadata, autoload_with=engine)
Review = db.Table('Reviews', metadata, autoload_with=engine)
Review_media = db.Table('Review_media', metadata, autoload_with=engine)
