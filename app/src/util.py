from app.lib.torhelp.proxy import RethinkdbProxy
from app import config

make_proxy_for_table = lambda Model, table: RethinkdbProxy(
    Model, config.DBCON, config.DBNAME, table
)
