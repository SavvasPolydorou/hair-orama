# pylint: disable= C0116,C0114,C0115
import os
from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"


# # Create an engine
# engine = create_engine(SQLALCHEMY_DATABASE_URI)

# # Test the connection
# try:
#     connection = engine.connect()
#     print("Database connection successful!")
#     connection.close()
# except Exception as e:
#     print(f"Error connecting to the database: {str(e)}")
SQLALCHEMY_TRACK_MODIFICATIONS = False
