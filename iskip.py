import os
import sys
import time
import requests
from datetime import datetime, timedelta, timezone


class TG:
    def __init__(self, token, chat_id, retry=2, timeout=5):
        # 检测是否为空
        if not token or not chat_id:
            raise ValueError("Token and chat_id cannot be empty")

        self.token = token
        self.chat_id = chat_id
        self.retry = retry
        self.timeout = timeout
        self.base = f"https://api.telegram.org/bot{token}"

    # 基础请求函数（带自动重试）
    def _post(self, method, data=None, files=None):
        url = f"{self.base}/{method}"
        for i in range(self.retry + 1):
            try:
                resp = requests.post(url, data=data, files=files, timeout=self.timeout)
                return resp.json()
            except Exception as e:
                if i == self.retry:
                    print(f"Telegram API 请求失败,{e}")
                    return {"ok": False, "error": str(e)}
                print(f"{e}\nTelegram API 请求失败，正在第 {i + 1} 次重试...")
                time.sleep(1)
        return None

    # 发文字
    def send_text(self, text, parse_mode=None):
        data = {
            "chat_id": self.chat_id,
            "text": text
        }
        if parse_mode:
            data["parse_mode"] = parse_mode
        return self._post("sendMessage", data=data)

    def send_markdown(self, text):
        return self.send_text(text, "Markdown")


def tg_send(msg):
    if "TG_CONFIG" not in os.environ:
        # 标准日志输出
        print('❌未添加TG_CONFIG变量')
        # 脚本退出
        sys.exit(0)
    tg_bot_token, tg_chat_id = os.getenv("TG_CONFIG").split(';')
    now_beijing = format_to_iso(datetime.now(timezone.utc) + timedelta(hours=8))

    if tg_bot_token and tg_chat_id:
        tg_bot = TG(tg_bot_token, tg_chat_id)

        msg = (f"\n"
               f"#quark *夸克自动签到*\n"
               f"\n"
               f"{msg}\n"
               f"\n"
               f"📅 *时间*：{now_beijing}\n")

        tg_bot.send_markdown(msg)


def format_to_iso(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')


def main():
    msg = "✴️ 今日已完成签到"
    tg_send(msg)


if __name__ == '__main__':
    print("----------今日已经签到----------")
    main()
    print("----------发送脚本通知----------")
