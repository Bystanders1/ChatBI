from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

from .llm_clients import sql_llm, interpretation_llm
from .database import db

# --- 这部分代码是正确的，保持不变 ---
DB_SCHEMA_INFO = db.get_table_info()
toolkit = SQLDatabaseToolkit(db=db, llm=sql_llm)
tools = toolkit.get_tools()
SYSTEM_PROMPT = f"""
你是一个专家级的MySQL数据分析AI助手。
你的目标是帮助用户通过自然语言与数据库进行交互。请严格遵循以下工作流程：
# 数据库结构信息 (你的永久记忆):
你将操作的数据库的表结构如下：
{DB_SCHEMA_INFO}
# 工作流程:
1.  **分析问题**: 首先，仔细分析用户的提问 `{{input}}`。
2.  **参考结构**: 你必须首先参考上面提供的“数据库结构信息”来构建SQL，而不是优先使用工具去勘查。
3.  **构建SQL**: 构建一条单一、高效且可执行的MySQL查询语句。
    - **核心规则：你必须一次只生成并执行一条SQL语句。如果用户的问题需要多个SQL才能回答，请只构建并执行解决其最核心问题的那一条。**
    - **安全和效率**: 绝对不要使用 `SELECT *`，只选择你需要的列。如果只需要几条示例数据，请使用 `LIMIT`。
    - **语法**: 所有表名和列名（尤其是中文名）都必须用反引号 (`) 包裹。
4.  **执行SQL**: 使用 `sql_db_query` 工具来执行查询。
5.  **解读结果 (至关重要!)**:
    - 你必须仔细分析 `sql_db_query` 工具返回的结果。
    - **如果结果是一个空列表 `[]`**: 这意味着数据库中没有找到符合条件的数据，请明确告知用户。
    - **如果结果只有一个条目/一行**: 这就是最终的、确切的答案！请直接根据这一行数据形成你的结论。
    - **如果结果有多行**: 请进行总结，并可以挑选前几条作为示例展示。
6.  **最终回答**: 基于你对结果的分析，用通俗、友好、清晰的中文回答用户的问题。
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
agent = create_openai_tools_agent(llm=sql_llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
interpretation_prompt = PromptTemplate.from_template(
    """
    基于以下信息，请为用户生成一段通俗易懂的中文总结。
    原始问题: {question}
    SQL查询结果: {sql_result}
    你的任务:
    1. 用自然的语言复述查询结果的关键信息。
    2. 不要暴露SQL查询语句或数据库的列名（如`姓名`, `工作单位`）。
    3. 如果结果是一个列表，清晰地列出关键项。
    4. 如果结果为空或没有信息，请友好地告知用户“根据数据，没有找到相关信息”。
    5. 总结应该简洁明了，直接回答用户的问题。
    生成的总结:
    """
)
interpretation_chain = interpretation_prompt | interpretation_llm


# ----------------- 🔴 最终修复：更新数据提取逻辑 🔴 -----------------
async def process_natural_language_query(question: str) -> dict:
    final_summary = "处理出现错误。"
    sql_query_executed = "未能提取SQL"
    raw_db_result = "未能提取原始数据"
    error_message = None

    try:
        agent_response = await agent_executor.ainvoke({"input": question})
        final_summary = agent_response.get("output", "未能生成总结。")

        if 'intermediate_steps' in agent_response and agent_response['intermediate_steps']:
            for step in reversed(agent_response['intermediate_steps']):
                action = step[0]
                observation = step[1]

                # 🔴 新的、更健壮的查找逻辑
                # 检查action对象是否有`tool_calls`属性，这是新版agent的特征
                if hasattr(action, 'tool_calls') and action.tool_calls:
                    for tool_call in action.tool_calls:
                        # 检查工具名是否是我们需要的
                        if tool_call.get('tool') == 'sql_db_query':
                            # 精准提取SQL语句和对应的观察结果
                            sql_query_executed = tool_call.get('args', {}).get('query', '未能从参数中提取SQL')
                            raw_db_result = observation
                            break  # 内层循环找到后就跳出

                # 如果找到了，外层循环也跳出
                if raw_db_result != "未能提取原始数据":
                    break

    except Exception as e:
        error_message = f"处理查询时发生错误: {str(e)}"
        final_summary = "抱歉，我在处理您的问题时遇到了一个内部错误。"
        print(f"Error processing query: {e}")

    return {
        "question": question,
        "summary": final_summary,
        "sql_query": sql_query_executed,
        "raw_data": raw_db_result,
        "error": error_message
    }