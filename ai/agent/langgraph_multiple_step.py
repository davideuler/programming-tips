# Agent执行工具调用与用户审核
# 这个项目展示了如何使用LangGraph构建一个Agent系统，在执行关键工具调用前允许用户审核和批准操作。

# 主要功能：
# 创建一个Agent执行工作流，包含计划、工具选择和执行步骤
# 在执行每一个工具调用前添加断点，等待用户确认
# 用户可以批准、拒绝或修改工具调用参数

# PYTHONPATH=$(pwd) uv run src/examples/langgraph_weather.py

from typing import TypedDict, List, Dict, Any, Annotated, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import os
import json


# 定义状态类型
class AgentState(TypedDict):
    messages: Annotated[List[Dict], "对话历史"]
    tools: Annotated[List[Dict], "可用工具列表"]
    tool_calls: Annotated[List[Dict], "待执行的工具调用"]
    tool_results: Annotated[List[Dict], "工具执行结果"]
    pending_tool_call_index: Annotated[Optional[int], "当前待确认/执行的工具索引"]

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
    new_state["tool_results"] = []
    new_state["pending_tool_call_index"] = None
    last_message = state["messages"][-1]["content"]
    
    # 添加系统消息指示LLM解析用户需求
    parse_message = f"""根据用户的请求: '{last_message}'，
    确定需要使用哪个或哪些工具来完成任务，并确定它们的执行顺序。可用工具有:
    {TOOLS}
    
    请返回一个JSON格式的列表，其中每个元素是一个工具调用描述。每个描述应包含 "name" (工具名) 和 "parameters" (参数字典)。
    例如:
    [
        {{"name": "search_weather", "parameters": {{"city": "北京"}}}},
        {{"name": "send_email", "parameters": {{"to": "example@example.com", "subject": "天气提醒", "content": "北京天气..."}}}}
    ]
    如果只需要一个工具，则列表中只包含一个元素。如果不需要工具，则返回一个空列表。
    """
    
    # 使用LLM解析请求
    response = llm.invoke([HumanMessage(content=parse_message)])
    
    # 解析LLM返回的工具调用列表
    try:
        # Attempt to repair common JSON issues from LLM output if direct parsing fails
        cleaned_response_content = response.content.strip()
        if cleaned_response_content.startswith("```json"): # Remove markdown fences
            cleaned_response_content = cleaned_response_content[7:]
        if cleaned_response_content.endswith("```"):
            cleaned_response_content = cleaned_response_content[:-3]
        cleaned_response_content = cleaned_response_content.strip()

        tool_calls_list = json.loads(cleaned_response_content)
        if isinstance(tool_calls_list, list) and all(isinstance(tc, dict) and "name" in tc and "parameters" in tc for tc in tool_calls_list):
            new_state["tool_calls"] = tool_calls_list
        elif isinstance(tool_calls_list, dict) and "name" in tool_calls_list and "parameters" in tool_calls_list: # Handle case where LLM returns a single dict instead of list
            new_state["tool_calls"] = [tool_calls_list]
        else:
            print(f"Warning: LLM response for tool calls was not a valid JSON list or dict of tool calls: {response.content}")
            new_state["tool_calls"] = []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from LLM response: {response.content}")
        new_state["tool_calls"] = [] # Default to no tool calls on error
        # Fallback logic (simplified)
        # Consider a more robust fallback or re-prompting the LLM here in a real application
        if "search_weather" in last_message.lower():
            city = "上海"
            if "北京" in last_message or "beijing" in last_message.lower(): city = "北京"
            new_state["tool_calls"].append({"name": "search_weather", "parameters": {"city": city}})
        if "email" in last_message.lower() and "send_email" in [t["name"] for t in TOOLS]:
             new_state["tool_calls"].append({
                "name": "send_email", 
                "parameters": {"to": "example@example.com", "subject": "自动邮件", "content": f"关于 {last_message} 的AI生成内容"}
            })

    if new_state.get("tool_calls"):
        new_state["pending_tool_call_index"] = 0 # Initialize index
        planned_tools_message = "我计划按顺序执行以下工具 (将逐个请求确认):"
        for i, tool_call in enumerate(new_state["tool_calls"]):
            planned_tools_message += f"\n{i+1}. 工具: {tool_call['name']}, 参数: {tool_call['parameters']}"
        new_state["messages"] = list(state["messages"]) + [
            {"role": "system", "content": planned_tools_message}
        ]
    else:
        # Only add this message if no tools were planned *and* no error message from LLM parsing was added previously.
        # This avoids duplicate messages if the JSON parsing itself printed an error.
        if not any(msg["role"] == "system" and "LLM response for tool calls was not a valid JSON" in msg["content"] for msg in new_state.get("messages", [])) and \
           not any(msg["role"] == "system" and "Error decoding JSON from LLM response" in msg["content"] for msg in new_state.get("messages", [])):
            new_state["messages"] = list(state["messages"]) + [
                {"role": "system", "content": "我没有找到合适的工具来处理您的请求，或者LLM未能正确规划工具。"}
            ]
    
    return new_state

def execute_single_tool(state: AgentState) -> AgentState:
    """执行当前待处理的单个工具调用并返回 mock 结果"""
    new_state = state.copy()
    
    if new_state.get("pending_tool_call_index") is None or \
       not isinstance(new_state.get("pending_tool_call_index"), int) or \
       new_state["pending_tool_call_index"] >= len(new_state.get("tool_calls", [])):
        new_state["messages"].append({"role": "system", "content": "错误：尝试执行工具但没有有效待处理的工具调用索引。"})
        return new_state

    current_tool_index = new_state["pending_tool_call_index"]
    tool_call_to_execute = new_state["tool_calls"][current_tool_index]
    
    name = tool_call_to_execute["name"]
    params = tool_call_to_execute["parameters"]
    
    result_content = ""
    if name == "search_weather":
        result_content = f"{params['city']}的天气今天是晴朗，温度25°C，适合外出活动。"
    elif name == "send_email":
        result_content = f"邮件已成功发送至{params['to']}，主题为：{params['subject']}"
    else:
        result_content = "不支持的工具调用"
            
    current_tool_result = {
        "tool_name": name,
        "parameters": params,
        "result": result_content
    }
    
    if not isinstance(new_state.get("tool_results"), list):
        new_state["tool_results"] = []
        
    new_state["tool_results"].append(current_tool_result)
    
    new_state["messages"] = list(new_state["messages"]) + [
        {"role": "system", "content": f"工具 '{name}' (参数: {params}) 执行完毕。结果: {result_content}"}
    ]
    
    new_state["pending_tool_call_index"] = current_tool_index + 1
    
    return new_state

def should_continue_tool_execution(state: AgentState) -> str:
    """判断是否还有待执行的工具"""
    tool_calls = state.get("tool_calls", [])
    pending_index = state.get("pending_tool_call_index")

    if pending_index is not None and isinstance(pending_index, int) and 0 <= pending_index < len(tool_calls):
        return "execute_single_tool"
    else:
        return "generate_response"

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
builder.add_node("execute_single_tool", execute_single_tool)
builder.add_node("generate_response", generate_response)

# 定义流程
builder.add_edge(START, "parse_input")

builder.add_conditional_edges(
    "parse_input",
    should_continue_tool_execution,
    {
        "execute_single_tool": "execute_single_tool",
        "generate_response": "generate_response"
    }
)
builder.add_conditional_edges(
    "execute_single_tool", 
    should_continue_tool_execution,
    {
        "execute_single_tool": "execute_single_tool", 
        "generate_response": "generate_response"
    }
)

builder.add_edge("generate_response", END)

# 设置内存存储和断点
memory = MemorySaver()
graph = builder.compile(checkpointer=memory, interrupt_before=["execute_single_tool"])

# 执行图
initial_state = {
    "messages": [{"role": "user", "content": "北京今天天气怎么样？天气情况发送到我邮箱 tom@test.com"}],
    "tools": TOOLS,
    "tool_calls": [],
    "tool_results": [],
    "pending_tool_call_index": None
}
thread = {"configurable": {"thread_id": "weather_query_multi_confirm_v2"}}

print("执行工作流直到第一个工具调用确认点...")
messages_printed_in_initial_stream = list(initial_state["messages"])
printed_planned_tools_from_initial_stream = False # To ensure we print planned tools only once

# This first graph.stream() call executes the initial part of the workflow (user input parsing, LLM-based tool planning)
#  up to the point where the first actual tool execution is about to happen and requires user confirmation.
for current_state_snapshot in graph.stream(initial_state, thread, stream_mode="values"):
    # current_state_snapshot is the full state after a step.
    # We don't have the specific "current node name" easily here for simple printing.
    # The loop runs until the first interruption.
    
    print("\n--- Graph processing step completed ---") # Generic message for each state update

    # Print new messages from the current state
    latest_messages = current_state_snapshot.get("messages", [])
    new_messages = [msg for msg in latest_messages if msg not in messages_printed_in_initial_stream]
    if new_messages:
        # print("New messages from this step:") # Can be verbose, direct print is often fine
        for msg in new_messages:
            print(f"- {msg['role']}: {msg['content']}")
    messages_printed_in_initial_stream = list(latest_messages) # Update baseline for next iteration

    # Check if 'parse_input' node has likely run and set up tool calls.
    # We infer this by checking if 'tool_calls' is populated and 'pending_tool_call_index' is 0.
    # And ensure we print this info only once during this initial stream.
    current_tool_calls = current_state_snapshot.get("tool_calls")
    current_pending_index = current_state_snapshot.get("pending_tool_call_index")

    if not printed_planned_tools_from_initial_stream and \
       current_tool_calls and \
       isinstance(current_pending_index, int) and current_pending_index == 0:
        
        print("---")
        print("LLM 已规划以下工具调用序列:")
        for i, tc in enumerate(current_tool_calls):
            print(f"  {i+1}. 工具: {tc['name']}, 参数: {tc['parameters']}")
        print("---")
        printed_planned_tools_from_initial_stream = True
    
    # This loop will break automatically when the graph hits an interrupt_before condition
    # (i.e., before 'execute_single_tool' if tools are planned).

# 用户反馈循环
while True:
    current_graph_state = graph.get_state(thread)
    if not current_graph_state:
        print("\n工作流意外结束 (状态丢失)。")
        break

    current_state_values = current_graph_state.values
    all_tool_calls = current_state_values.get("tool_calls", [])
    current_tool_idx = current_state_values.get("pending_tool_call_index")
    next_nodes_to_execute = current_graph_state.next # This is a tuple of next possible nodes

    if not next_nodes_to_execute: # Graph has finished naturally
        print("\n工作流已执行完毕 (无后续节点)。")
        # Final messages might have been printed by the last node in the stream above or need a final print here
        final_messages_in_state = current_state_values.get("messages", [])
        new_final_messages = [msg for msg in final_messages_in_state if msg not in messages_printed_in_initial_stream]
        if new_final_messages:
            print("最后阶段新消息:")
            for msg in new_final_messages:
                print(f"- {msg['role']}: {msg['content']}")
        break

    # Check if the graph is waiting for confirmation before execute_single_tool
    if "execute_single_tool" in next_nodes_to_execute and \
       current_tool_idx is not None and isinstance(current_tool_idx, int) and 0 <= current_tool_idx < len(all_tool_calls):
        
        tool_to_confirm = all_tool_calls[current_tool_idx]
        print(f"\n--- 用户确认 ({current_tool_idx + 1}/{len(all_tool_calls)}) ---")
        print(f"系统计划执行工具: {tool_to_confirm['name']}")
        print(f"参数: {tool_to_confirm['parameters']}")
        
        try:
            user_approval = input("确认执行此工具调用? (yes/no/cancel_all): ").lower()
        except EOFError: # Handle non-interactive environments
            print("非交互式环境，自动批准。")
            user_approval = "yes"
        except Exception:
            user_approval = "yes" # Default for other errors during input

        state_update_needed = False
        state_to_update = current_state_values.copy()
        stream_after_decision = False

        if user_approval == "yes":
            print("\n用户已批准，继续执行此工具...")
            # No state change needed by the user interaction loop itself for 'yes'. Graph will proceed.
            stream_after_decision = True
        elif user_approval == "cancel_all":
            print("\n用户已取消所有剩余工具调用。")
            state_to_update["pending_tool_call_index"] = len(all_tool_calls) # Set index out of bounds
            state_to_update["messages"].append({"role": "system", "content": "用户取消了剩余的工具调用。"})
            state_update_needed = True
            stream_after_decision = True # Stream to process this state change and go to generate_response
        else: # "no" or any other input treated as no
            print(f"\n用户已拒绝执行工具 '{tool_to_confirm['name']}'。跳过此工具并取消后续工具。")
            state_to_update["pending_tool_call_index"] = len(all_tool_calls) # Skip all subsequent
            state_to_update["messages"].append({"role": "system", "content": f"用户拒绝执行工具 '{tool_to_confirm['name']}'。后续工具调用已取消。"})
            state_update_needed = True
            stream_after_decision = True # Stream to process this state change

        if state_update_needed:
            graph.update_state(thread, state_to_update)
            messages_printed_in_initial_stream = list(state_to_update["messages"]) # Update baseline for new messages
        
        if stream_after_decision:
            print(f"\n--- Streaming graph after user decision: {user_approval} ---") # Added for clarity
            #  graph.stream(None, ...) calls are responsible for running one or more steps of the graph from its last interruption point, 
            # based on user decisions or state modifications, until the next interruption is hit or the graph concludes.
            for current_state_snapshot_after_decision in graph.stream(None, thread, stream_mode="values"):
                print("\n--- Graph processing step after user decision ---") # Generic step message
                latest_messages = current_state_snapshot_after_decision.get("messages", [])
                new_messages = [msg for msg in latest_messages if msg not in messages_printed_in_initial_stream]
                if new_messages:
                    for msg in new_messages:
                        print(f"- {msg['role']}: {msg['content']}")
                messages_printed_in_initial_stream = list(latest_messages) # Update baseline correctly         
            
            if user_approval != "yes": 
                break 
            continue
        else: # Should not happen if logic is correct, but as a fallback to prevent infinite loop if no streaming decision
            print("内部逻辑错误：未决定是否继续流式处理。")
            break

    elif "generate_response" in next_nodes_to_execute:
        print("\n所有工具已处理完毕或被跳过，准备生成最终回复...")
        for event in graph.stream(None, thread, stream_mode="values"):
            for node_name, node_state_output in event.items():
                print(f"\n执行节点: {node_name}")
                if "messages" in node_state_output:
                    new_messages = [msg for msg in node_state_output["messages"] if msg not in messages_printed_in_initial_stream]
                    for msg in new_messages:
                        print(f"- {msg['role']}: {msg['content']}")
                    messages_printed_in_initial_stream = list(node_state_output["messages"])        
        break # Exit the confirmation loop as graph should run to END now
    else:
        # This case implies the graph has ended or is in an unexpected state where .next is not 'execute_single_tool' or 'generate_response'
        print("\n工作流已完成，或处于未预期的中断状态。")
        final_messages_in_state_unexpected = current_graph_state.values.get("messages", [])
        new_final_messages_unexpected = [msg for msg in final_messages_in_state_unexpected if msg not in messages_printed_in_initial_stream]
        if new_final_messages_unexpected:
            print("当前状态中的新消息:")
            for msg in new_final_messages_unexpected:
                 print(f"- {msg['role']}: {msg['content']}")
        break # Exit loop

print("\n--- 工作流结束 ---")
