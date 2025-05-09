# https://page1.genspark.site/page/toolu_01U6t1p8UiuWbmqtdwNBQup1/ai_agent_frameworks_tutorial.html

# 通过两个代理（Assistant和UserProxy）的协作，完成股票数据分析和可视化任务。代理们通过对话交流，生成代码、执行代码、优化结果，直到完成任务。

# 主要功能：
# 获取META和TESLA股票的年初至今收益率
# 绘制股票价格变化图表
# 代理之间自动迭代优化代码直至成功执行
# 使用 yfinance 需要设置代理 (export all_proxy=http://127.0.0.1:8080)

# uv pip install yfinance matplotlib "ag2[openai]>=0.8.4"
# PYTHONPATH=$(pwd) uv run src/examples/ag2_stock_analysis.py

import autogen
import os

# 配置模型和API密钥
# 创建AutoGen配置
def create_autogen_config(model_name="gpt-4o"):

    config_list = [
        {
            "api_type": "openai", 
            "model": os.getenv("OPENAI_MODEL") or model_name, 
            "api_key": os.environ.get("OPENAI_API_KEY", ""),
            "base_url" : os.getenv("OPENAI_BASE_URL")
        }
    ]
    
    # 如果没有设置API密钥，使用本地模型配置
    if not config_list[0]["api_key"]:
        config_list = [{"model": "llama3"}]
    
    return config_list

config_list = create_autogen_config()

# 创建"assistant"代理
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "cache_seed": 42,  # seed用于缓存中间结果
        "config_list": config_list, 
        "temperature": 0,  
    },  
)

# 创建"user_proxy"代理
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # 无需人工参与
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",  # 代码执行的工作目录
        "use_docker": False,   # 是否使用Docker执行代码
    },
)

# 启动对话，用户代理向助手提出任务
user_proxy.initiate_chat(
    assistant,
    message="""What date is today? Compare the year-to-date gain for META and TESLA. Should get price by yfinance or ALPHAVANTAGE through environment variable ALPHAVANTAGE_API_KEY.""",
)

# 继续对话，要求绘制图表
user_proxy.send(
    recipient=assistant,
    message="""Plot a chart of their stock price change YTD and save to stock_price_ytd.png.""",
)
