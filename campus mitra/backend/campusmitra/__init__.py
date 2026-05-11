# PyMySQL patch for local MySQL development only
import os
if not os.environ.get('DATABASE_URL'):
    try:
        import pymysql
        pymysql.version_info = (2, 2, 1, 'final', 0)
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
