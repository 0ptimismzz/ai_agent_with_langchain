from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.code_agent.model.config import API_KEY

llm_qwen = ChatOpenAI(
    model="qwen-max-latest",
    # model="qwen3-235b-a22b",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr(API_KEY),
    streaming=True,
)