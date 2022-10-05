# Test Description

I have:

* an __M1__ Mac
* Python 3.10.6
* Running a SqlServer database under Docker:

```
docker run --name sqlsvr-container --net dev-network -p 1433:1433 -d apilogicserver/sqlsvr-m1:version1.0.0
```

<figure><img src="./images/docker-container.png"></figure>

I am able to configure and connect with Azure Data Studio:

<figure><img src="./images/AzureDataStudio-connects.png"></figure>

While Azure Data Studio did not require it, I also configured the database for remote access:

```
EXEC sp_configure 'remote access', 1;
RECONFIGURE
```

I have installed the ODBC driver (per [this doc](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16)), like this:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18
```

When running this app with the following connect string:

```python
# times out: engine = create_engine("mssql+pyodbc://sa:MyPass@word@sqlsvr-container:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes")
engine = create_engine("mssql+pyodbc://sa:MyPass@word@localhost:1433/NORTHWND?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=no&Encrypt=no")
```

It gets _connection refused_, I suspect due to odbc install/configure.:

```log
(venv) val@Vals-MPB-14 sqlsvr-m1 %  cd /Users/val/dev/examples/sqlsvr-m1 ; /usr/bin/env /Users/val/dev/examples/sqlsvr
-m1/venv/bin/python /Users/val/.vscode-insiders/extensions/ms-python.python-2022.14.0/pythonFiles/lib/python/debugpy/a
dapter/../../debugpy/launcher 62414 -- run.py 
Traceback (most recent call last):
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3250, in _wrap_pool_connect
....
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 597, in connect
    return self.dbapi.connect(*cargs, **cparams)
pyodbc.OperationalError: ('HYT00', '[HYT00] [Microsoft][ODBC Driver 18 for SQL Server]Login timeout expired (0) (SQLDriverConnect)')

(venv) val@Vals-MPB-14 sqlsvr-m1 % 
```

The issue is [logged here](https://github.com/sqlalchemy/sqlalchemy/discussions/8604).

## ODBC Driver procedure

Using [this article (thanks!)](https://whodeenie.medium.com/installing-pyodbc-and-unixodbc-for-apple-silicon-8e238ed7f216), we use the following procedure/

#### 1. Download `pyodbc-4.0.32.tar.gz`

I had to unpack it (perhaps due to unfamiliarity with tar files):

<figure><img src="https://github.com/valhuber/sqlsvr-m1/blob/main/images/pyodbc.png?raw=true"></figure>


#### 2. Verify `unixodbc`

```
val@Vals-MPB-14 ~ %  brew install unixodbc
Running `brew update --auto-update`...
==> Auto-updated Homebrew!
Updated 1 tap (homebrew/core).
==> New Formulae
curlcpp

Warning: unixodbc 2.3.11 is already installed and up-to-date.
```

It's here:

<figure><img src="https://github.com/valhuber/sqlsvr-m1/blob/main/images/unixodbc.png?raw=true"></figure>


#### 3. Rebuild `pyodbc'

And alter the provided rebuild script:

```
pip uninstall pyodbc
export CPPFLAGS="-I/opt/homebrew/Cellar/unixodbc/2.3.11/include"
export LDFLAGS="-L/opt/homebrew/Cellar/unixodbc/2.3.11/lib -liodbc -liodbcinst"
echo "path/to/pyodbc-4.0.32.tar.gz"
cd /Users/val/dev/pyodbc
echo "pip install pyodbc-4.0.32.tar.gz failed -- no gz?"
pip install pyodbc
```

and then run in the venv:

```
(venv) val@Vals-MPB-14 pyodbc % pip install pyodbc       
Collecting pyodbc
  Using cached pyodbc-4.0.34.tar.gz (271 kB)
  Preparing metadata (setup.py) ... done
Using legacy 'setup.py install' for pyodbc, since package 'wheel' is not installed.
Installing collected packages: pyodbc
  Running setup.py install for pyodbc ... done
Successfully installed pyodbc-4.0.34

(venv) val@Vals-MPB-14 pyodbc % pip freeze
pyodbc==4.0.34
SQLAlchemy==1.4.29
(venv) val@Vals-MPB-14 pyodbc % 
```

#### Opens DB, but no tables, reflect fails

`run.py` does open the database, but no tables and relect fails

<figure><img src="https://github.com/valhuber/sqlsvr-m1/blob/main/images/no-tables.png?raw=true"></figure>

&nbsp;

## Basic ODBC

Tried a non-SQLAlchemy connection per Gord Thompson suggestion (thankyou!).  It also just exits without a stacktrace:

<figure><img src="https://github.com/valhuber/sqlsvr-m1/blob/main/images/basic_odbc.png?raw=true"></figure>

