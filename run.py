import sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData
import sqlalchemy.dialects.postgresql.base as pg_dialect
from sqlalchemy import CHAR, Column, DateTime, Float, ForeignKey, Index, Integer, String, TIMESTAMP, Table, Text, UniqueConstraint, text

# db: docker run --name sqlsvr-container --net dev-network -p 1433:1433 -d apilogicserver/sqlsvr-m1:version1.0.0

engine = create_engine("mssql+pyodbc://SA:MyPass@word@sql:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no")

metadata = MetaData(engine)
metadata.reflect(engine)

print("open with metadata")