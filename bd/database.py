import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

sqliteName = 'movies.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))

#SQLite
databaseUrl = f'sqlite:///{os.path.join(base_dir, sqliteName)}'
engine = create_engine(databaseUrl, echo =True)

#MySQL
#mysql+<drivername>://<username>:<password>@<server>:<port>/dbname

#connection_string = "mysql+mysqlconnector://root:@localhost:3306/sqlalchemy"
#engine = create_engine(connection_string, echo=True)

#Postgres


#url = "postgresql+psycopg2://postgres:Grvn240675$$@localhost:5432/movies"
#engine = create_engine(url, echo=True)

# url = URL.create(
#     drivername="postgresql",
#     username="postgres",
#     password="Grvn240675$$",
#     host="localhost",
#     database="movies"
# )


SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
