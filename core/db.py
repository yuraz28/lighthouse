import databases
import ormar
import sqlalchemy

mysql_dsn = (
    "mysql+mysqlconnector://root:password@localhost/kod23"
)

metadata = sqlalchemy.MetaData()
database = databases.Database(mysql_dsn)
engine = sqlalchemy.create_engine(mysql_dsn)


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata
