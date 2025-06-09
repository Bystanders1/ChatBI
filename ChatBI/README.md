# ChatBI 后端服务

这是一个基于 LangChain 和 FastAPI 的后端服务，可以将自然语言转换为对 MySQL 数据库的 SQL 查询，并对结果进行人性化解读。

## 🚀 快速开始

### 1. 环境准备

-   确保你已安装 Python 3.9+。
-   确保你的 MySQL 数据库正在运行。

### 2. 安装依赖

在 `ChatBI` 根目录下，创建一个虚拟环境并安装所有必需的包：

```bash
# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` (如果你创建了一个) 或直接创建 `.env` 文件，并填写你的配置信息：

```dotenv
# 数据库URL
DB_URL="mysql+mysqlconnector://user:password@hostname:port/database_name"

# Hugging Face API Token
HUGGINGFACEHUB_API_TOKEN="hf_xxxxxxxx"

# 兼容OpenAI的API配置
OPENAI_API_BASE="[https://api.your-provider.com/v1](https://api.your-provider.com/v1)"
OPENAI_API_KEY="sk-xxxxxxxx"
OPENAI_MODEL_NAME="your-model-name"
```

### 4. 运行服务

使用 uvicorn 启动 FastAPI 应用：

```bash
uvicorn app.main:app --reload
```

-   `--reload` 参数会在代码变更后自动重启服务，非常适合开发环境。
-   服务将默认运行在 `http://127.0.0.1:8000`。

### 5. 测试 API

服务启动后，你可以在浏览器中访问 `http://127.0.0.1:8000/docs` 查看由 FastAPI 自动生成的 Swagger UI 文档。

你可以在文档页面直接测试 `/api/v1/query` 端点。

**请求示例 (JSON Body):**
```json
{
  "question": "最近6个月请假最多的员工是谁？"
}
```

---

**下一步**：您可以开始搭建前端项目了。前端只需向 `http://127.0.0.1:8000/api/v1/query` 发送 POST 请求，并将结果展示出来即可。 