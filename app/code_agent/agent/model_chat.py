import uuid

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory, FileChatMessageHistory
from langchain_community.agent_toolkits.file_management import FileManagementToolkit
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableWithMessageHistory, RunnableSequence

from app.code_agent.model.qwen import llm_qwen
from app.code_agent.prompts.multi_chat_prompts import multi_chat_prompt

store = {}

def get_session_history(session_id: str):
    # 老版本实现
    # if session_id not in store:
    #     store[session_id] = ChatMessageHistory()
    # # print(store)
    # return store[session_id]
    return FileChatMessageHistory("/Users/horizon/Desktop/project/ai_agent/app/code_agent/chat_history/"+f"{session_id}.json")

file_toolkit = FileManagementToolkit(root_dir="/Users/horizon/Desktop/project/ai_agent/.temp")
file_tools = file_toolkit.get_tools()

# code_agent = create_react_agent(
#     model=llm_qwen,
#     tools=file_tools
# )
llm_with_tools = llm_qwen.bind_tools(tools=file_tools)

# 串行写法一
# chain = multi_chat_prompt | llm_with_tools | StrOutputParser()
# 串行写法二
# chain = multi_chat_prompt.pipe(llm_with_tools).pipe(StrOutputParser())
# 串行写法三
chain = RunnableSequence(
    first=multi_chat_prompt,
    middle=[llm_with_tools],
    last=StrOutputParser()
)

chain_with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

chat_session_id = uuid.uuid4()

while True:
    user_input = input("用户：")
    if user_input.lower() == "exit" or user_input.lower() == "quit":
        break

    response = chain_with_history.stream(
        {"question":user_input},
        config={"configurable":{"session_id":chat_session_id}},
    )
    print("助理：",end="")
    for chunk in response:
        print(chunk,end="")
    print("\n")

# chat_history = ChatMessageHistory()
# chat_history.add_user_message(HumanMessage(content="我叫Horizon"))
#
# for chunk in chain.stream({"question":"你是谁？","chat_history":chat_history.messages}):
#     print(chunk,end="")