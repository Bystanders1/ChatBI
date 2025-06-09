import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """
    应用配置类。
    """
    # 数据库配置
    DB_URL: str

    # OpenAI 兼容 API 配置
    OPENAI_API_BASE: str
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


# 创建一个全局可用的配置实例
settings = Settings()