from pydantic import BaseModel
from typing import Optional, Any

class QueryRequest(BaseModel):
    """
    用户查询请求的数据模型
    """
    question: str
    # conversation_id: Optional[str] = None # 可选，用于支持多轮对话

class QueryResponse(BaseModel):
    """
    API 响应的数据模型
    """
    question: str
    summary: str
    sql_query: str
    raw_data: Any #可以是列表、字典等
    error: Optional[str] = None