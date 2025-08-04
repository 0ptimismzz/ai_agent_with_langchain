import re
import subprocess
import time

from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

# 清除markdown字符串
def clean_bash_tags(s):
    s = re.sub(r'^\s*```bash\s*', '', s, flags=re.DOTALL)
    s = re.sub(r'^\s*```shell\s*', '', s, flags=re.DOTALL)
    s = re.sub(r'^\s*```\s$', '', s, flags=re.DOTALL)
    return s.strip()

def run_applescript(script):
    p = subprocess.Popen(["osascript", "-e", script],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()

    return output.decode("utf-8").strip(), err.decode("utf-8").strip()

def run_script(script):
    output, error = run_applescript(script)
    if error:
        print("\nrun_script error:")
        print(error)
        print("-" * 60)
    return output, error

def get_all_terminal_window_ids():
    output, error = run_script("""
tell application "Terminal"
    set outputList to {}
    repeat with aWindow in windows
        set windowID to id of aWindow
        set tabCount to number of tabs of aWindow
        repeat with tabIndex from 1 to tabCount
            set end of outputList to {tab tabIndex of window id windowID}
        end repeat
    end repeat
end tell
return outputList
""")
    if error:
        return error
    else:
        if "," in output:
            list_data = output.split(",")
            list_data = [item.strip() for item in list_data]
        else:
            list_data = [output.strip()]
        return list_data

@mcp.tool(name="close_terminal", description="关闭终端应用程序")
def close_terminal_if_open():
    output, error = run_script("""
tell application "System Events"
    if exists process "Terminal" then
        tell application "Terminal" to quit
    end if
end tell 
""")
    if error:
        return False
    else:
        return True

@mcp.tool(name="open_terminal", description="打开新的终端窗口")
def open_new_terminal(args: str = "") -> str:
    output, error = run_script(f"""
tell application "Terminal"
    if (count of windows) > 0 then
        activate
    else
        activate
    end if
end tell
""")
    time.sleep(5)
    if error:
        return error
    else:
        if output.strip() == "":
            return get_all_terminal_window_ids()[0]
        else:
            return output

@mcp.tool(name="run_script_in_terminal", description="向终端内输入脚本")
def run_script_in_terminal(command: str) -> str:
    command = clean_bash_tags(command)
    print("\nrun_script_in_terminal command:")
    print(command)
    print("-" * 60)
    output, error = run_applescript(f"""
tell application "Terminal"
    activate
    if (count of windows) > 0 then
        do script "{command}" in window 1
    else
        do script "{command}"
    end if
end tell
""")
    if error:
        return error
    else:
        return output

@mcp.tool(name="get_terminal_full_text", description="获取终端的显示内容")
def get_terminal_full_text():
    output, error = run_script(f"""
tell application "Terminal"
    set fullText to history of selected tab of front window
end tell
""")
    if error:
        return error
    else:
        return output

if __name__ == "__main__":
    mcp.run(transport="stdio")


