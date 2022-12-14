import sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy import CHAR, Column, DateTime, Float, ForeignKey, Index, Integer, String, TIMESTAMP, Table, Text, UniqueConstraint, text

# db: docker run --name sqlsvr-container --net dev-network -p 1433:1433 -d apilogicserver/sqlsvr-m1:latest

# times out: engine = create_engine("mssql+pyodbc://sa:Posey3861d@sqlsvr-container:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes")

engine = create_engine("mssql+pyodbc://sa:Posey3861@localhost:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no")

metadata = MetaData(engine)  # opens db..
metadata.reflect(engine)  # meta data shows no tables, exits here without message

print("open with metadata")