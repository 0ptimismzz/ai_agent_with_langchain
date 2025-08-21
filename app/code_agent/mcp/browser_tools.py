import re
import time

from bs4 import BeautifulSoup, Comment

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mcp.server.fastmcp import FastMCP


mcp = FastMCP()

@mcp.tool(description="search query word in sogou")
def search_in_sogou(query: str) -> str:
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.sogou.com/")

        text_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "query"))
        )

        text_box.send_keys(query)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "stb"))
        )
        submit_button.click()

        WebDriverWait(driver, 5).until(
            EC.title_contains(query[:10])
        )

        # 翻页优化
        page_text_list = []
        for i in range(1):
            if i>0:
                page_container = WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.ID, "pagebar_container"))
                )
                # 在容器内查找所有a标签
                results = page_container.find_elements(By.TAG_NAME, "a")
                if i==1:
                    results[i-1].click()
                else:
                    results[i].click()
                time.sleep(1)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "main"))
            )

            # 滚动优化
            window_roll(driver)

            page_content = driver.find_element(By.ID, "main")
            page_text = page_content.get_attribute("innerHTML")
            page_text_list.append(f"第{i+1}页\n" + page_text + "\n --- \n")
        # return page_content.get_attribute("innerHTML")
        driver.quit()
        html = '\n'.join(page_text_list)
        return pretty_html(html)
    except Exception as e:
        print(e)
        return ""

def pretty_html(html: str) -> str:
    # 190792
    # 119136
    # 74900
    # 46873
    # 24806
    # 移除指定标签
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "link", "meta", "symbol", "path", "canvas", "svg"]):
        tag.extract()

    # 移除所有display：none的标签
    display_none_re = re.compile(r"display\s*:\s*none", re.IGNORECASE)
    for tag in soup.find_all(True):
        style = tag.get("style", "")
        if display_none_re.search(style):
            tag.extract()
    # 移除所有代码注释
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    # 移除无用属性
    for tag in soup.find_all(True):
        if tag.name == "a":
            if "href" in tag.attrs:
                if "javascript" in tag.attrs["href"] or "/" == tag.attrs["href"]:
                    tag.extract()
                else:
                    tag.attrs = {"href": tag.attrs["href"]}
        else:
            tag.attrs = {}
    html = soup.prettify()
    print(len(html))
    return html

def window_roll(driver):
    last_high = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        # 检查是否加载完成
        new_high = driver.execute_script("return document.body.scrollHeight")
        if new_high == last_high:
            break
        last_high = new_high

if __name__ == "__main__":
    mcp.run(transport="stdio")
    # content = search_in_sogou("西安天气怎么样")
    # print(content)