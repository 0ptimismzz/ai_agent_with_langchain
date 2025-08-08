import sys
import os

import hashlib
import alibabacloud_bailian20231229.client as bailian_20231229_client
import requests

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
INDEX_ID = "u0u422y24x"

mcp = FastMCP()

CATEGORY_ID = "cate_8154f9463834490390006dfbebdf2bcb_12123047"

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

def calculate_md5(file_path: str) -> str:
    """
    计算文件的 MD5 哈希值。

    参数:
        file_path (str): 文件路径。

    返回:
        str: 文件的 MD5 哈希值。
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# @mcp.tool(name="query_rag", description="从百炼平台查询知识库信息")
# def query_rag_from_bailian(query: str) -> str:
#     bailian_client = create_client()
#     rag = retrieve_index(bailian_client, WORKSPACE_ID, INDEX_ID, query)
#     result = ""
#     for data in rag.body.data.nodes:
#         result += f"""{data.text}
# ---"""
#
#     # print("=" * 60)
#     # print("[query_rag_from_bailian]", query)
#     # print(result)
#     # print("=" * 60)
#     return result

def apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id):
    headers = {}
    runtime = util_models.RuntimeOptions()
    request = bailian_20231229_models.ApplyFileUploadLeaseRequest(
        file_name=file_name,
        md_5=file_md5,
        size_in_bytes=file_size,
    )
    return client.apply_file_upload_lease_with_options(category_id, workspace_id, request, headers, runtime)

def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_md5 = calculate_md5(file_path)
    return file_name, file_size, file_md5

def apply_lease_by_file_path(client, category_id, workspace_id, file_path):
    file_name, file_size, file_md5 = get_file_info(file_path)
    return apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id)

def upload_file_to_bailian(upload_url, headers, file_path):
    with open(file_path, "rb") as f:
        file_content = f.read()

    upload_headers = {
        "Content-Type": headers["Content-Type"],
        "X-bailian-extra": headers["X-bailian-extra"],
    }

    response = requests.put(upload_url, data=file_content, headers=upload_headers)
    print(response.status_code)
    response.raise_for_status()

def add_file_to_balian_category(client, lease_id, parser, category_id, workspace_id):
    headers = {}
    runtime = util_models.RuntimeOptions()

    requests = bailian_20231229_models.AddFileRequest(
        lease_id=lease_id,
        parser=parser,
        category_id=category_id,
    )

    return client.add_file_with_options(workspace_id, requests, headers, runtime)

def describe_file(client, workspace_id, file_id):
    headers = {}
    runtime = util_models.RuntimeOptions()
    return client.describe_file_with_options(workspace_id, file_id, headers, runtime)

def create_index(client, workspace_id, name, file_id, structure_type="unstructured", source_type="DATA_CENTER_FILE", sink_type="BUILT_IN"):
    headers = {}
    runtime = util_models.RuntimeOptions()
    request = bailian_20231229_models.CreateIndexRequest(
        structure_type=structure_type,
        source_type=source_type,
        sink_type=sink_type,
        name=name,
        document_ids=[file_id],
    )
    return client.create_index_with_options(workspace_id, request, headers, runtime)

def submit_index(client, workspace_id, index_id):
    headers = {}
    runtime = util_models.RuntimeOptions()
    submit_index_job_request = bailian_20231229_models.SubmitIndexJobRequest(index_id=index_id)

    return client.submit_index_job_with_options(workspace_id, submit_index_job_request, headers, runtime)

def get_index_job_status(client, workspace_id, index_id, job_id):
    headers = {}
    runtime = util_models.RuntimeOptions()

    get_index_job_status_request = bailian_20231229_models.GetIndexJobStatusRequest(
        index_id=index_id,
        job_id=job_id,
    )

    return client.get_index_job_status_with_options(workspace_id, get_index_job_status_request, headers, runtime)

def list_indices(client, workspace_id):
    headers = {}
    runtime = util_models.RuntimeOptions()
    list_indices_request = bailian_20231229_models.ListIndicesRequest()
    return client.list_indices_with_options(workspace_id, list_indices_request, headers, runtime)

def submit_index_add_documents_job(client, workspace_id, index_id, file_id, source_type="DATA_CENTER_FILE"):
    headers = {}
    runtime = util_models.RuntimeOptions()
    submit_index_add_documents_job_request = bailian_20231229_models.SubmitIndexAddDocumentsJobRequest(
        index_id=index_id,
        document_ids=[file_id],
        source_type=source_type,
    )
    return client.submit_index_add_documents_job_with_options(workspace_id, submit_index_add_documents_job_request, headers, runtime)

def upload_rag_file_to_balian(client, category_id, workspace_id, file_path):
    """
    上传文件到百炼数据中心，并添加指定分类

    参数：
        client：百炼客户端
        workspace_id：业务空间id
        category_id：分类id
        file_path：文件路径
    返回：
        文件上传状态
    """
    print("=" * 100)
    # 1.申请文件租约
    lease = apply_lease_by_file_path(client, category_id, workspace_id, file_path)
    headers = lease.body.data.param.headers
    lease_id = lease.body.data.file_upload_lease_id
    upload_url = lease.body.data.param.url
    print("-" * 60)
    print("文件租约申请成功：")
    print("headers:", headers)
    print("lease_id", lease_id)
    print("upload_url", upload_url)
    print("-" * 60)
    print()

    # 2.上传文件至百炼数据中心
    upload_file_to_bailian(upload_url, headers, file_path)

    # 3.将文件添加到指定分类
    add_file_response = add_file_to_balian_category(client, lease_id, "DASHSCOPE_DOCMIND", category_id, workspace_id)
    file_id = add_file_response.body.data.file_id
    print("-" * 60)
    print("添加分类成功：")
    print("file_id:", file_id)
    print("-" * 60)
    print()

    # 4.获取文件上传状态
    describe_file_response = describe_file(client, workspace_id, file_id)
    print("-" * 60)
    print("文件上传状态：")
    print("body:", describe_file_response.body)
    print("-" * 60)
    print("=" * 100)

    return file_id

def add_document_to_index(client, workspace_id, index_id, file_id):
    job_response = submit_index_add_documents_job(client, workspace_id, index_id, file_id)
    job_id = job_response.body.data.id

    job_status = get_index_job_status(client, workspace_id, index_id, job_id)
    return job_status.body.data

@mcp.tool(name="query_rag", description="从百炼平台查询知识库信息")
def query_rag_from_bailian(query: str) -> str:
    bailian_client = create_client()
    rag = retrieve_index(bailian_client, WORKSPACE_ID, INDEX_ID, query)
    result = ""
    for data in rag.body.data.nodes:
        result += f"""{data.text}
---"""
    return result

@mcp.tool(name="upload_local_file_to_bailian_rag", description="将本地的知识文件上传到百炼平台知识库")
def upload_rag_to_bailian(file_path):
    bailian_client = create_client()
    file_id = upload_rag_file_to_balian(bailian_client, CATEGORY_ID, WORKSPACE_ID, file_path)
    return add_document_to_index(bailian_client, WORKSPACE_ID, INDEX_ID, file_id)

@mcp.tool(name="query_bailian_rag_job_status", description="查询上传到百炼知识库中知识文件的处理状态")
def query_bailian_rag_job_status(job_id):
    bailian_client = create_client()
    job_status = get_index_job_status(bailian_client, WORKSPACE_ID, INDEX_ID, job_id)
    return job_status.body.data

if __name__ == '__main__':
    mcp.run(transport="stdio")
