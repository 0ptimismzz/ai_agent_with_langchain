from langchain_community.agent_toolkits import FileManagementToolkit

file_toolkit = FileManagementToolkit(root_dir="/Users/horizon/Desktop/project/new_agent/.temp")
file_tools = file_toolkit.get_tools()