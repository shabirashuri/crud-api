from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from sqlalchemy.ext.declarative import declarative_base# type: ignore


URL_DATABASE = "mysql+pymysql://myuser:mypassword@localhost:3306/fastapi_1"

engine = create_engine(URL_DATABASE)


Sessionlocal = sessionmaker(autocommit = False ,autoflush = False,bind = engine)

Base  = declarative_base()

