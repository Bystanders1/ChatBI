from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import endpoints
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# 创建 FastAPI 应用实例
app = FastAPI(title="ChatBI - Natural Language to SQL API")

# 配置 CORS 中间件，允许所有来源的跨域请求
# 在生产环境中，建议将 origins 设置为你的前端域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# 包含 API 路由
# 给路由添加前缀 /api/v1
app.include_router(endpoints.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    """
    根路径，用于健康检查或欢迎信息。
    """
    return {"message": "Welcome to ChatBI API. Visit /docs for documentation."}