"""
下载云班课中加入课程的资源
"""

import urllib.request
import urllib.parse
import http.cookiejar
import json
import re


# 登录账号
def login(account: str, password: str):
    url = "https://coreapi-proxy.mosoteach.cn/index.php/passports/account-login"
    # 创建 Post 请求数据
    values = {"account": account, "password": password}
    post_data = json.dumps(values)
    # 发起 Post 请求
    response = urllib.request.urlopen(url, post_data.encode('utf8'))
    # 获取返回的 Json 数据
    administrator = json.loads(response.read().decode('utf8'))
    # 若账号密码错误，返回 False
    if not administrator["status"]:
        print(administrator["errorMessage"] + "，请重新输入账号和密码")
        return False
    else:
        # 获取当前用户的 Cookie
        token = administrator["token"]
        url = f"https://www.mosoteach.cn/web/index.php?c=passport&m=save_proxy_token&proxy_token={token}&remember_me=N"
        urllib.request.urlopen(url)
        return True


# 获取加入的课程
def get_joined_course():
    url = "https://www.mosoteach.cn/web/index.php?c=clazzcourse&m=my_joined"
    response = urllib.request.urlopen(url)
    course = json.loads(response.read().decode('utf8'))
    return course


# 获取选择课程的资源
def get_course_res(course_id: str):
    url = f"https://www.mosoteach.cn/web/index.php?c=res&m=index&clazz_course_id={course_id}"
    response = urllib.request.urlopen(url)
    result: str = response.read().decode('utf8')
    result = result[result.find("<div id=\"res-list-box\">"):result.find("<div id=\"down-book-box\">")]
    items = result.split("res-type manual-order")
    resources = []
    _regex_name = "title=(.*?)<"
    _regex_url = "data-href=\"[\\S]+\""
    for i in range(len(items) - 1):
        _item = items[i]
        # 匹配资源的名称
        _value = re.search(_regex_name, _item)
        _resource_name = _value.group()[_value.group().find(">") + 1:-1]
        # 匹配资源的链接
        _value = re.search(_regex_url, _item)
        _resource_url = _value.group()[11:-1]
        # 添加到 Json 列表中
        resources.append(json.dumps({"res_name": _resource_name, "res_url": _resource_url}))
    return resources


# 下载选择的资源
def download_res(resource: json):
    urllib.request.urlretrieve(resource["res_url"], resource["res_name"])


if __name__ == '__main__':
    # 启用 Cookie
    cookie = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    urllib.request.install_opener(opener)
    # 登录账号
    while True:
        _account = input("请输入账号：")
        _password = input("请输入密码：")
        if login(_account, _password):
            break
    # 获取加入的课程
    courses = get_joined_course()
    # 显示加入的课程
    courses_count = 0
    courses_id = []  # 记录加入的课程 ID
    print("索引\t课程名称")
    for item in courses["data"]:
        _course_name = item["course"]["name"]
        _course_id = item["id"]
        courses_id.append(_course_id)
        print(f"{courses_count + 1}\t{_course_name}")
        courses_count += 1
    # 获取用户选择的课程索引
    select_index = 0
    while True:
        select_index = int(input("请输入待下载的课程索引号："))
        if 1 <= select_index <= courses_count:
            break
        else:
            print("输入的索引无效，请重新输入")
    # 获取用户选择课程的资源
    res = get_course_res(courses_id[select_index - 1])
    # 显示用户选择课程的资源
    print("索引\t资源名称")
    for index in range(len(res)):
        item = json.loads(res[index])
        _res_name = item["res_name"]
        print(f"{index + 1}\t{_res_name}")
    # 获取用户选择课程资源的索引
    select_index = 0
    while True:
        select_index = int(input("请输入待下载的资源索引号："))
        if 1 <= select_index <= len(res):
            break
        else:
            print("输入的索引无效，请重新输入")
    # 下载选择的资源
    download_res(json.loads(res[select_index]))