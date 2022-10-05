import pyodbc

cnxn = pyodbc.connect(
    "Driver=ODBC Driver 18 for SQL Server;"
    "Server=localhost;"
    "Encrypt=No;"
    "UID=sa;PWD=MyPass@word;"  # adjust as required
    "Database=NORTHWND;"
)
print("Connected.")   # never gets here... no stacktrace
print("Examine cnxn")