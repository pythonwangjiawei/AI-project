import requests
import queue
import time

API_KEY = "API_KEY"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL_NAME = "glm-4-flash"
message_history = []

# 请求队列 & 限流配置
request_queue = queue.Queue()
RATE_LIMIT_INTERVAL = 0.8
last_request_time = 0 

def zhipu_api_request(payload):
    global last_request_time

    request_queue.put(payload)

    while not request_queue.empty():
        task_data = request_queue.get()

        now = time.time()
        gap = now - last_request_time
        if gap < RATE_LIMIT_INTERVAL:
            time.sleep(RATE_LIMIT_INTERVAL - gap)

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(API_URL, headers=headers, json=task_data, timeout=60)
            last_request_time = time.time()
            res_json = response.json()

# 字段校验
            if response.status_code != 200:
                return f"接口请求失败，状态码:{response.status_code}, 返回:{res_json}"

            if "choices" not in res_json or len(res_json["choices"]) == 0:
                return "【数据异常】服务端返回数据缺失choices字段，数据乱序，本次请求丢弃"

            ai_content = res_json["choices"][0]["message"]["content"]
            return ai_content

        except requests.exceptions.Timeout:
            return "【异常】请求超时，服务器长时间无响应"
        except Exception as e:
            return f"【异常】网络或者解析出错：{str(e)}"
        finally:
            request_queue.task_done()

def chat_with_zhipu(user_input):
    message_history.append({"role": "user", "content": user_input})
    request_data = {
        "model": MODEL_NAME,
        "messages": message_history,
        "temperature": 0.7
    }
    reply = zhipu_api_request(request_data)

    if not reply.startswith("【"):
        message_history.append({"role": "assistant", "content": reply})
    return reply


if __name__ == "__main__":
    print("=" * 50)
    print("智谱GLM-4-Flash 命令行对话（增加队列限流+返回字段校验版）")
    print("输入 quit 退出对话")
    print("=" * 50)
    while True:
        user_text = input("\n【你】：")
        if user_text.strip().lower() == "quit":
            print("对话结束，程序退出")
            break
        ai_response = chat_with_zhipu(user_text)
        print(f"\n【GLM-4-Flash】：{ai_response}")
