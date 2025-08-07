import re
import subprocess
import time
from typing import List

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

def parse_key_code(button):
    button = button.lower()

    keycode_map = {
        'return': 'return',
        'space': 'space',
        'up': 126,
        'down': 125,
        'left': 123,
        'right': 124,
        'a': 0,
        'b': 11,
        'c': 8,
        'd': 2,
        'e': 14,
        'f': 3,
        'g': 5,
        'h': 4,
        'i': 34,
        'j': 38,
        'k': 40,
        'l': 37,
        'm': 46,
        'n': 45,
        'o': 31,
        'p': 35,
        'q': 12,
        'r': 15,
        's': 1,
        't': 17,
        'u': 32,
        'v': 9,
        'w': 13,
        'x': 7,
        'y': 16,
        'z': 6,
        '.': 47,
        'dot': 47,
        '0': 29,
        '1': 18,
        '2': 19,
        '3': 20,
        '4': 21,
        '5': 23,
        '6': 22,
        '7': 26,
        '8': 28,
        '9': 25,
        '-': 27,
    }

    return keycode_map[button]

def concat_key_codes(key_codes):
    script = ''
    for key in key_codes:
        key_code = parse_key_code(key)
        if isinstance(key_code, int):
            script += f'\t\tkey code {key_code}\n'
        else:
            script += f'\t\tkeystroke {key_code}\n'
        script += '\t\tdelay 0.5\n'
    return script.strip()

@mcp.tool(name="send_terminal_keyboard_key", description="向终端输入一组按键")
def send_terminal_keyboard_key(key_codes: List[str]) -> bool:
    print('\nsend_terminal_keyboard_key keycode:', key_codes)
    print('-' * 50)
    script = f"""
tell application "Terminal"
    activate
    tell application "System Events"
        {concat_key_codes(key_codes)}
    end tell
end tell
"""
    print(script)
    terminal_content, error = run_script(script)
    if error:
        return False
    else:
        return True

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
    send_terminal_keyboard_key(["up", "return"])
    # mcp.run(transport="stdio")


