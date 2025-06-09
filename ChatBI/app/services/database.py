from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from app.core.config import settings

# 创建数据库连接引擎
# connect_args 是为了确保 SQLAlchemy 能正确处理某些字符集
engine = create_engine(settings.DB_URL, connect_args={"charset": "utf8"})

# 创建 LangChain 使用的数据库实例
# 这个实例可以帮助 LangChain 获取数据库的 schema 信息
db = SQLDatabase(engine=engine)

def get_db():
    """
    返回一个 LangChain 数据库实例。
    未来可以扩展为数据库连接池的管理。
    """
    return db