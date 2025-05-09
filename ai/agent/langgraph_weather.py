
# Agent执行工具调用与用户审核
# 这个项目展示了如何使用LangGraph构建一个Agent系统，在执行关键工具调用前允许用户审核和批准操作。

# 主要功能：
# 创建一个Agent执行工作流，包含计划、工具选择（单个工具）和执行步骤
# 在执行工具调用前添加断点，等待用户确认
# 用户可以批准、拒绝或修改工具调用参数

# PYTHONPATH=$(pwd) uv run src/examples/langgraph_weather.py

from typing import TypedDict, List, Dict, Any, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import os


# 定义状态类型
class AgentState(TypedDict):
    messages: Annotated[List[Dict], "对话历史"]
    tools: Annotated[List[Dict], "可用工具列表"]
    tool_calls: Annotated[List[Dict], "待执行的工具调用"]
    tool_results: Annotated[List[Dict], "工具执行结果"]

# 模拟工具定义
TOOLS = [
    {
        "name": "search_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "city": "要查询天气的城市名称"
        }
    },
    {
        "name": "send_email",
        "description": "发送电子邮件给指定收件人",
        "parameters": {
            "to": "收件人邮箱地址",
            "subject": "邮件主题",
            "content": "邮件内容"
        }
    }
]

# 设置LLM
llm = ChatOpenAI(model="gpt-4o", api_key=os.environ["OPENAI_API_KEY"], base_url=os.getenv("OPENAI_BASE_URL"))

# 定义节点函数
def parse_user_input(state: AgentState) -> AgentState:
    """解析用户输入并确定下一步操作"""
    new_state = state.copy()
    last_message = state["messages"][-1]["content"]
    
    # 添加系统消息指示LLM解析用户需求
    parse_message = f"""根据用户的请求: '{last_message}'，
    确定需要使用哪个工具来完成任务。可用工具有:
    {TOOLS}
    
    请返回一个工具调用描述，格式为:
    工具名称: <工具名>
    参数: <参数字典>
    """
    
    # 使用LLM解析请求
    response = llm.invoke([HumanMessage(content=parse_message)])
    
    # 模拟工具调用解析
    tool_name = None
    tool_params = {}
    
    if "search_weather" in response.content.lower():
        tool_name = "search_weather"
        # 简单解析参数（实际应用中需要更复杂的解析）
        if "北京" in last_message or "beijing" in last_message.lower():
            tool_params = {"city": "北京"}
        else:
            tool_params = {"city": "上海"}  # 默认值
    
    elif "send_email" in response.content.lower():
        tool_name = "send_email"
        tool_params = {
            "to": "example@example.com",
            "subject": "自动生成的邮件",
            "content": "这是由AI助手生成的邮件内容。"
        }
    
    if tool_name:
        new_state["tool_calls"] = [{
            "name": tool_name,
            "parameters": tool_params
        }]
    
    # 添加系统消息解释选择的工具
    new_state["messages"] = list(state["messages"]) + [
        {"role": "system", "content": f"我将使用 {tool_name} 工具，参数为: {tool_params}"}
    ]
    
    return new_state

def execute_tool(state: AgentState) -> AgentState:
    """执行工具调用并返回结果"""
    new_state = state.copy()
    tool_calls = state.get("tool_calls", [])
    
    results = []
    for tool_call in tool_calls:
        name = tool_call["name"]
        params = tool_call["parameters"]
        
        # 模拟工具执行
        if name == "search_weather":
            result = f"{params['city']}的天气今天是晴朗，温度25°C，适合外出活动。"
        elif name == "send_email":
            result = f"邮件已成功发送至{params['to']}，主题为：{params['subject']}"
        else:
            result = "不支持的工具调用"
            
        results.append({
            "tool_name": name,
            "result": result
        })
    
    new_state["tool_results"] = results
    
    # 添加结果到消息中
    new_state["messages"] = list(state["messages"]) + [
        {"role": "system", "content": f"工具执行结果: {results[0]['result']}"}
    ]
    
    return new_state

def generate_response(state: AgentState) -> AgentState:
    """基于工具执行结果生成最终回复"""
    new_state = state.copy()
    
    # 构建上下文消息
    context_messages = []
    for msg in state["messages"]:
        if msg["role"] == "user":
            context_messages.append(HumanMessage(content=msg["content"]))
        else:
            context_messages.append(AIMessage(content=msg["content"]))
    
    # 生成总结回复
    response = llm.invoke(context_messages + [
        HumanMessage(content="根据以上信息，生成一个简洁的用户回复。")
    ])
    
    new_state["messages"] = list(state["messages"]) + [
        {"role": "assistant", "content": response.content}
    ]
    
    return new_state

# 构建图
builder = StateGraph(AgentState)
builder.add_node("parse_input", parse_user_input)
builder.add_node("execute_tool", execute_tool)
builder.add_node("generate_response", generate_response)

# 定义流程
builder.add_edge(START, "parse_input")
builder.add_edge("parse_input", "execute_tool")
builder.add_edge("execute_tool", "generate_response")
builder.add_edge("generate_response", END)

# 设置内存存储和断点
memory = MemorySaver()
# 在execute_tool前添加断点，等待用户确认
graph = builder.compile(checkpointer=memory, interrupt_before=["execute_tool"])

# 执行图
initial_state = {
    "messages": [{"role": "user", "content": "北京今天天气怎么样？"}],
    "tools": TOOLS,
    "tool_calls": [],
    "tool_results": []
}
thread = {"configurable": {"thread_id": "weather_query"}}

# 运行图直到断点
print("执行工作流直到断点...")
for event in graph.stream(initial_state, thread, stream_mode="values"):
    print(f"\n执行节点: {event.get('step_name', '未知节点')}")
    if "messages" in event:
        for msg in event["messages"]:
            print(f"- {msg['role']}: {msg['content']}")
    if "tool_calls" in event and event["tool_calls"]:
        print(f"待执行工具: {event['tool_calls'][0]['name']}")
        print(f"参数: {event['tool_calls'][0]['parameters']}")

# 用户反馈
try:
    print("\n需要用户确认:")
    print("系统将执行工具调用，是否批准？")
    user_approval = input("确认执行工具调用? (yes/no): ")
except:
    user_approval = "yes"  # 默认值用于自动测试

# 基于用户反馈继续或终止
if user_approval.lower() == "yes":
    print("\n用户已批准，继续执行...")
    for event in graph.stream(None, thread, stream_mode="values"):
        print(f"\n执行节点: {event.get('step_name', '未知节点')}")
        if "messages" in event:
            for msg in event["messages"]:
                if msg not in initial_state["messages"]:  # 只显示新消息
                    print(f"- {msg['role']}: {msg['content']}")
else:
    print("\n操作被用户取消。")
