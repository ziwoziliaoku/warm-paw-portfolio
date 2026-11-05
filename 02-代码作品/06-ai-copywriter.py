# 06-ai-copywriter.py
# 暖爪咖啡 · AI 文案生成器 v3（真 AI 版）
# 用豆包大模型现场写文案

import os
from openai import OpenAI

# ====== API Key 从环境变量读取（不要把真实 key 写进代码） ======
API_KEY = os.getenv("ARK_API_KEY")
if not API_KEY:
    raise ValueError("没有读取到 ARK_API_KEY，请先配置环境变量。")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

print("=" * 45)
print("  暖爪咖啡 · AI 文案生成器（真 AI 版）")
print("=" * 45)
print()

product = input("请输入产品名：")
season = input("请输入季节（秋日/冬日/春日/夏日）：")
style = input("请输入风格（治愈/活力/高级）：")
print()
print("AI 正在思考中...")
print()

# 把你的需求拼成一段指令发给 AI
prompt = f"""你是一个咖啡品牌文案专家。请为以下产品写一段海报文案：

产品名：{product}
季节：{season}限定
风格：{style}
品牌：暖爪咖啡 WARM PAW（可爱治愈系小熊猫IP）

请输出：
1. 主标题（一句话，8-12字，有画面感）
2. 副标题（一句话，产品名+卖点）
3. 一句品牌口号（slogan）
4. 三个卖点关键词（用顿号隔开）

格式简洁，不要多余解释。"""

# 调用豆包大模型
response = client.chat.completions.create(
    model=os.getenv("ARK_MODEL"),  # 推理接入点 ID（从环境变量读取）
    messages=[
        {"role": "system", "content": "你是一个专业的咖啡品牌文案写手，风格温暖可爱。"},
        {"role": "user", "content": prompt}
    ]
)

# 打印 AI 返回的文案
print("=" * 45)
print("  【AI 生成的海报文案】")
print("=" * 45)
print()
print(response.choices[0].message.content)
print()
print("=" * 45)

input("\n按回车键退出...")
