from fastapi import APIRouter, HTTPException
from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_processor import process_natural_language_query

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    接收前端的自然语言查询请求，并返回处理结果。
    """
    if not request.question:
        raise HTTPException(status_code=400, detail="查询问题不能为空")

    try:
        result = await process_natural_language_query(request.question)
        return QueryResponse(**result)
    except Exception as e:
        # 兜底的异常处理
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")