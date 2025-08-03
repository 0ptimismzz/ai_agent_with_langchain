from tkinter.scrolledtext import example

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, ChatMessagePromptTemplate,FewShotPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from app.bailian.config import API_KEY

llm = ChatOpenAI(
    model="qwen-max-latest",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr(API_KEY),
    streaming=True,
)

# prompt_template = PromptTemplate.from_template("今天{something}真不错")
#
# prompt = prompt_template.format(something="天气")
#
# resp = llm.stream(prompt)
# for chunk in resp:
#     print(chunk.content, end="")

system_message_template = ChatMessagePromptTemplate.from_template(
    template="你是一位{role}专家,擅长回答{domain}领域问题",
    role="system",
)

human_message_template = ChatMessagePromptTemplate.from_template(
    template="用户问题:{question}",
    role="user",
)

# 创建提示词模板
chat_prompt_template = ChatPromptTemplate.from_messages([
    system_message_template,
    human_message_template,
])

prompt = chat_prompt_template.format_messages(
    role="编程",
    domain="Web开发",
    question="如何构建一个基于SpringBoot的后端应用？"
)
examples = [
    {"input":"将'hello'翻译成中文","output":"你好"},
    {"input":"将'goodbye'翻译成中文","output":"再见"}
]
example_template = "输入：{input}\n输出：{output}"
few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=PromptTemplate.from_template(example_template),
    prefix="请将以下英文翻译成中文",
    suffix="输入：{text}\n输出：",
    input_variables=["text"]
)
prompt = few_shot_prompt_template.format(text="Thank you for your time!")
print(prompt)
# resp = llm.stream(prompt)
chain = few_shot_prompt_template | llm
resp = chain.stream(input={"text":"good morning"})
for chunk in resp:
    print(chunk.content, end="")

