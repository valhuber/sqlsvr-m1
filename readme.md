# Objective - Reference Example for Mac M1, SqlServer, Python

It appears there has been a good deal of struggle to get this working.  This project is intended to provide the smallest possible sample - a reference implementation.

This documents 3 procedures for testing SqlServer access on an M1 mac.

&nbsp;

# Background

I have:

* an __M1__ Mac
* Python 3.10.6 (via Python.org)
* Running a SqlServer database under Docker, created from `mcr.microsoft.com/mssql/server`:

```
docker run --name sqlsvr-container --net dev-network -p 1433:1433 -d apilogicserver/sqlsvr-m1:version1.0.2
```

<figure><img src="https://github.com/valhuber/sqlsvr-m1/blob/main/images/docker-container.png?raw=true"></figure>

I am able to configure and connect with Azure Data Studio:

<figure><img src="https://github.com/valhuber/sqlsvr-m1/blob/main/images/AzureDataStudio-connects.png?raw=true"></figure>

While Azure Data Studio did not require it, I also configured the database for remote access:

```
EXEC sp_configure 'remote access', 1;
RECONFIGURE
```

&nbsp;

# "Standard" Procedure for SQLAlchemy - worked

I have installed the ODBC driver (per [this doc](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16)), like this:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18
```
I then created a `venv` in the standard manner:

```
python3 -m pip install -r requirements.txt
```
&nbsp;

The `Run SQLAlchemy` launch successfully opens the database and discovers tables:

<figure><img src="https://github.com/valhuber/sqlsvr-m1/blob/main/images/standard-procedure-runs.png?raw=true"></figure>

The issue is [logged here](https://github.com/sqlalchemy/sqlalchemy/discussions/8604).

&nbsp;


# Basic ODBC - worked

Also tried a non-SQLAlchemy connection, per Gord Thompson suggestion (thankyou!). 


Appears to run:

<figure><img src="https://github.com/valhuber/sqlsvr-m1/blob/main/images/basic-odbc-runs.png?raw=true"></figure>

&nbsp;

# Appendix: "Ed King" ODBC Driver procedure

I also attempted, without luck, the procedure below...

&nbsp;

&nbsp;

Using [this article (many thanks!!)](https://whodeenie.medium.com/installing-pyodbc-and-unixodbc-for-apple-silicon-8e238ed7f216), we used this procedure:

### 1. Download `pyodbc-4.0.32.tar.gz` into `project/pyodbc`

I had to unpack it (perhaps due to unfamiliarity with tar files):

<figure><img src="https://github.com/valhuber/sqlsvr-m1/blob/main/images/pyodbc.png?raw=true"></figure>


### 2. Brew install `unixodbc` and rebuild `pyodbc`

Execute this procedure as shown in the screen shot above:

```
cd pyodbc
sh rebuild-pyodbc.sh
```

Observe `Unixodbc` is here:

<figure><img src="https://github.com/valhuber/sqlsvr-m1/blob/main/images/unixodbc.png?raw=true"></figure>


### Opens DB, but no tables, reflect fails

`run.py` does open the database, but no tables and reflect fails:

<figure><img src="https://github.com/valhuber/sqlsvr-m1/blob/main/images/no-tables.png?raw=true"></figure>
