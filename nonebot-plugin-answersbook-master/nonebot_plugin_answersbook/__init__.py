﻿import random
from pathlib import Path

from nonebot import on_endswith, on_startswith
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.matcher import Matcher

__zx_plugin_name__ = "答案之书"
__plugin_usage__ = """
usage：
    寻求答案
    指令：
        翻看答案 + 问题，问题 + 翻看答案
""".strip()
__plugin_des__ = "答案之书"
__plugin_type__ = ("群内小游戏",)
__plugin_cmd__ = ["翻看答案 + 问题，问题 + 翻看答案"]
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["答案之书写", "答案"],
}

try:
    import ujson as json
except ModuleNotFoundError:
    import json

answers_path = Path(__file__).parent / "answersbook.json"
answers = json.loads(answers_path.read_text("utf-8"))

def get_answers():
    key = random.choice(list(answers))
    return answers[key]["answer"]

answers_starts = on_startswith("翻看答案")
answers_ends = on_endswith("翻看答案")

@answers_starts.handle()
@answers_ends.handle()
async def answersbook(event: GroupMessageEvent, matcher: Matcher):
    msg = event.message.extract_plain_text().replace("翻看答案", "")
    if not msg:
        await matcher.finish("你想问什么问题呢？")
    answer = get_answers()
    await matcher.send(answer, at_sender=True)
