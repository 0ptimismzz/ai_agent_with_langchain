from langchain_core.output_parsers import StrOutputParser,CommaSeparatedListOutputParser

from app.bailian.common import chat_prompt_template,llm

# parser = StrOutputParser()
parser = CommaSeparatedListOutputParser()

chain = chat_prompt_template | llm | parser

resp = chain.invoke(input={
    "role":"计算",
    "domain":"数学计算",
    "question":"100+2*100=?,(不使用markdown格式)"
})

print(resp)