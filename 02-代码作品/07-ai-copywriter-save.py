# 07-ai-copywriter-save.py
# 暖爪咖啡 · AI 文案生成器 v4（自动保存 + 批量版）
# 新概念：文件写入、for 循环

import os
from openai import OpenAI
from datetime import datetime

API_KEY = os.getenv("ARK_API_KEY")
if not API_KEY:
    raise ValueError("没有读取到 ARK_API_KEY，请先配置环境变量。")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

print("=" * 45)
print("  暖爪咖啡 · AI 文案生成器 v4（批量+保存）")
print("=" * 45)
print()

season = input("请输入季节（秋日/冬日/春日/夏日）：")
style = input("请输入风格（治愈/活力/高级）：")
print()
print("请输入产品名，多个用逗号隔开（比如：雪绒热可可,肉桂苹果拿铁,蜜桃冷萃）：")
products = input("> ").replace("，", ",").split(",")
products = [p.strip() for p in products if p.strip()]  # 去掉空格和空项
print()

# 准备保存文件
filename = f"暖爪文案库-{season}-{datetime.now().strftime('%Y%m%d-%H%M')}.txt"
saved_lines = []  # 把所有文案存起来，最后一起写入文件

for product in products:
    print(f"正在为「{product}」生成文案...")

    prompt = f"""你是咖啡品牌文案专家。为以下产品写海报文案：
产品名：{product}
季节：{season}限定
风格：{style}
品牌：暖爪咖啡 WARM PAW（小熊猫IP，治愈系）

请输出：主标题、副标题、品牌slogan、三个卖点关键词。格式简洁。"""

    try:
        r = client.chat.completions.create(
            model=os.getenv("ARK_MODEL"),  # 推理接入点 ID（从环境变量读取）
            messages=[
                {"role": "system", "content": "你是温暖可爱的咖啡品牌文案。"},
                {"role": "user", "content": prompt}
            ]
        )
        text = r.choices[0].message.content
        print(f"✅ 完成")
        print(text)
        print()
        # 加入保存列表
        saved_lines.append(f"【{product}】\n{text}\n{'='*40}\n")
    except Exception as e:
        print(f"❌ 失败：{e}")
        print()

# 一次性写入文件
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"暖爪咖啡 · {season}文案库\n生成时间：{datetime.now()}\n\n")
    f.writelines(saved_lines)

print("=" * 45)
print(f"全部完成！文案已保存到：{filename}")
print("=" * 45)

input("\n按回车键退出...")
