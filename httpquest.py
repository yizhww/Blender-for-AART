import requests

url = 'https://yizhww.github.io/Blender-for-AART/index.json'
try:
    response = requests.get(url)
    response.raise_for_status()  # 检查响应状态码
    data = response.json()
    print(data)
except requests.exceptions.HTTPError as http_err:
    if response.status_code == 404:
        print(f"请求的文件 {url} 未找到。")
    else:
        print(f"HTTP错误发生: {http_err}")
except Exception as err:
    print(f"其他错误发生: {err}")