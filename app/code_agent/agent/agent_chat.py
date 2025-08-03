from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.redis import RedisSaver
from langgraph.prebuilt import create_react_agent

from app.code_agent.model.qwen import llm_qwen
from app.code_agent.tools.file_tools import file_tools


def create_agent():
    # 本地内存记忆
    # memory = MemorySaver()
    # agent = create_react_agent(
    #     model=llm_qwen,
    #     tools=file_tools,
    #     checkpointer=memory,
    #     debug=True,
    # )
    #
    # return agent

    # Redis缓存
    with RedisSaver.from_conn_string("redis://localhost:6379" ) as memory:
        memory.setup()
        agent = create_react_agent(
            model=llm_qwen,
            tools=file_tools,
            checkpointer=memory,
            debug=False,
        )

        return agent

def run_agent():
    config = RunnableConfig(configurable={"thread_id":1})

    agent = create_agent()

    while True:
        user_input = input("用户：")
        if user_input == "exit":
            break
        res = agent.invoke(input={"messages": user_input},config=config)

        print("助理：", end="")
        print(res["messages"][-1].content)
        print("\n")


if __name__ == "__main__":
    run_agent()