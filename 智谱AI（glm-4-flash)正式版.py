import requests

API_KEY = "API_KEY"

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

MODEL_NAME = "glm-4-flash"

message_history = []


def chat_with_zhipu(user_input):
    message_history.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    request_data = {
        "model": MODEL_NAME,
        "messages": message_history,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=request_data, timeout=60)
        result = response.json()

        if response.status_code == 200:
            ai_reply = result["choices"][0]["message"]["content"]
            message_history.append({"role": "assistant", "content": ai_reply})
            return ai_reply
        else:
            error_msg = f"接口调用失败！状态码：{response.status_code}，返回内容：{result}"
            return error_msg

    except Exception as e:
        return f"网络异常：{str(e)}"


if __name__ == "__main__":
    print("=" * 50)
    print("智谱GLM-4-Flash 命令行连续对话")
    print("输入 quit 退出对话")
    print("=" * 50)

    while True:
        user_text = input("\n【你】：")
        if user_text.strip().lower() == "quit":
            print("对话结束，程序退出")
            break
        ai_response = chat_with_zhipu(user_text)
        print(f"\n【GLM-4-Flash】：{ai_response}")