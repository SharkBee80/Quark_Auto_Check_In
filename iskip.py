import os
import sys
from datetime import datetime, timedelta, timezone

from tg import TG


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

        msg = f"""
#quark *夸克自动签到*

{msg}

📅 *时间*：{now_beijing}
        """

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
