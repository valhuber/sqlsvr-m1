# Test Description


I have a SqlServer database, running on __M1__ Mac, under Docker:

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
dapter/../../debugpy/launcher 62131 -- run.py 
Traceback (most recent call last):
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3250, in _wrap_pool_connect
    return fn()
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 310, in connect
    return _ConnectionFairy._checkout(self)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 868, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 476, in checkout
    rec = pool._do_get()
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 145, in _do_get
    with util.safe_reraise():
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 70, in __exit__
    compat.raise_(
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/util/compat.py", line 207, in raise_
    raise exception
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 143, in _do_get
    return self._create_connection()
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 256, in _create_connection
    return _ConnectionRecord(self)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 371, in __init__
    self.__connect()
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 665, in __connect
    with util.safe_reraise():
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 70, in __exit__
    compat.raise_(
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/util/compat.py", line 207, in raise_
    raise exception
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 661, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 590, in connect
    return dialect.connect(*cargs, **cparams)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 597, in connect
    return self.dbapi.connect(*cargs, **cparams)
pyodbc.OperationalError: ('HYT00', '[HYT00] [Microsoft][ODBC Driver 18 for SQL Server]Login timeout expired (0) (SQLDriverConnect)')

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "/Users/val/.vscode-insiders/extensions/ms-python.python-2022.14.0/pythonFiles/lib/python/debugpy/adapter/../../debugpy/launcher/../../debugpy/__main__.py", line 39, in <module>
    cli.main()
  File "/Users/val/.vscode-insiders/extensions/ms-python.python-2022.14.0/pythonFiles/lib/python/debugpy/adapter/../../debugpy/launcher/../../debugpy/../debugpy/server/cli.py", line 430, in main
    run()
  File "/Users/val/.vscode-insiders/extensions/ms-python.python-2022.14.0/pythonFiles/lib/python/debugpy/adapter/../../debugpy/launcher/../../debugpy/../debugpy/server/cli.py", line 284, in run_file
    runpy.run_path(target, run_name="__main__")
  File "/Users/val/.vscode-insiders/extensions/ms-python.python-2022.14.0/pythonFiles/lib/python/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_runpy.py", line 321, in run_path
    return _run_module_code(code, init_globals, run_name,
  File "/Users/val/.vscode-insiders/extensions/ms-python.python-2022.14.0/pythonFiles/lib/python/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_runpy.py", line 135, in _run_module_code
    _run_code(code, mod_globals, init_globals,
  File "/Users/val/.vscode-insiders/extensions/ms-python.python-2022.14.0/pythonFiles/lib/python/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_runpy.py", line 124, in _run_code
    exec(code, run_globals)
  File "run.py", line 14, in <module>
    metadata.reflect(engine)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/sql/schema.py", line 4697, in reflect
    with inspection.inspect(bind)._inspection_context() as insp:
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/inspection.py", line 64, in inspect
    ret = reg(subject)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/reflection.py", line 182, in _engine_insp
    return Inspector._construct(Inspector._init_engine, bind)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/reflection.py", line 117, in _construct
    init(self, bind)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/reflection.py", line 128, in _init_engine
    engine.connect().close()
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3204, in connect
    return self._connection_cls(self, close_with_result=close_with_result)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 96, in __init__
    else engine.raw_connection()
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3283, in raw_connection
    return self._wrap_pool_connect(self.pool.connect, _connection)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3253, in _wrap_pool_connect
    Connection._handle_dbapi_exception_noconnection(
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 2100, in _handle_dbapi_exception_noconnection
    util.raise_(
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/util/compat.py", line 207, in raise_
    raise exception
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3250, in _wrap_pool_connect
    return fn()
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 310, in connect
    return _ConnectionFairy._checkout(self)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 868, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 476, in checkout
    rec = pool._do_get()
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 145, in _do_get
    with util.safe_reraise():
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 70, in __exit__
    compat.raise_(
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/util/compat.py", line 207, in raise_
    raise exception
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 143, in _do_get
    return self._create_connection()
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 256, in _create_connection
    return _ConnectionRecord(self)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 371, in __init__
    self.__connect()
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 665, in __connect
    with util.safe_reraise():
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 70, in __exit__
    compat.raise_(
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/util/compat.py", line 207, in raise_
    raise exception
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 661, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 590, in connect
    return dialect.connect(*cargs, **cparams)
  File "/Users/val/dev/examples/sqlsvr-m1/venv/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 597, in connect
    return self.dbapi.connect(*cargs, **cparams)
sqlalchemy.exc.OperationalError: (pyodbc.OperationalError) ('HYT00', '[HYT00] [Microsoft][ODBC Driver 18 for SQL Server]Login timeout expired (0) (SQLDriverConnect)')
(Background on this error at: https://sqlalche.me/e/14/e3q8)
(venv) val@Vals-MPB-14 sqlsvr-m1 % 
```

The issue is [logged here](https://github.com/sqlalchemy/sqlalchemy/discussions/8592).