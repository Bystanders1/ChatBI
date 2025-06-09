from langchain_openai import ChatOpenAI
from app.core.config import settings


def get_text_to_sql_llm():
    """
    初始化并返回用于 Text-to-SQL 的LLM。
    使用与解读模型相同的 OpenAI 兼容 API。
    为了保证SQL生成的准确性，可以将温度设置得低一些。
    """
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL_NAME,
        openai_api_key=settings.OPENAI_API_KEY,
        openai_api_base=settings.OPENAI_API_BASE,
        temperature=0.0, # 设为0.0以获得更稳定、确定性的SQL输出
    )
    return llm

def get_interpretation_llm():
    """
    初始化并返回用于结果解读的、兼容OpenAI API的LLM。
    """
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL_NAME,
        openai_api_key=settings.OPENAI_API_KEY,
        openai_api_base=settings.OPENAI_API_BASE,
        temperature=0.7,
    )
    return llm

# 实例化 LLMs
# 注意：现在两个llm变量都指向了ChatOpenAI的实例
sql_llm = get_text_to_sql_llm()
interpretation_llm = get_interpretation_llm()