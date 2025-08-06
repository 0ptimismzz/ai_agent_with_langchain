import sys
import os

import alibabacloud_bailian20231229.client as bailian_20231229_client

# from app.code_agent.rag.config import WORKSPACE_ID, INDEX_ID, alibaba_access_key, alibaba_access_secret
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_tea_util import models as util_models
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP

load_dotenv()

alibaba_access_key = os.getenv("ALIBABA_CLOUD_ACCESS_KEY")
alibaba_access_secret = os.getenv("ALIBABA_CLOUD_ACCESS_SECRET")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")
INDEX_ID = os.getenv("INDEX_ID")


mcp = FastMCP()

def create_client() -> bailian_20231229_client.Client:
    access_key = alibaba_access_key
    access_secret = alibaba_access_secret
    config = open_api_models.Config(
        access_key_id=access_key,
        access_key_secret=access_secret,
    )
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian_20231229_client.Client(config)

def retrieve_index(client, workspace_id, index_id, query):
    retrieve_request = bailian_20231229_models.RetrieveRequest(
        index_id=INDEX_ID,
        query=query,
    )
    runtime = util_models.RuntimeOptions()
    return client.retrieve_with_options(
        workspace_id,
        retrieve_request,
        {},
        runtime,
    )

@mcp.tool(name="query_rag", description="从百炼平台查询知识库信息")
def query_rag_from_bailian(query: str) -> str:
    bailian_client = create_client()
    rag = retrieve_index(bailian_client, WORKSPACE_ID, INDEX_ID, query)
    result = ""
    for data in rag.body.data.nodes:
        result += f"""{data.text}
---"""

    # print("=" * 60)
    # print("[query_rag_from_bailian]", query)
    # print(result)
    # print("=" * 60)
    return result

if __name__ == '__main__':
    mcp.run(transport="stdio")
