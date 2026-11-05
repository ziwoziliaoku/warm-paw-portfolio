# 05-copywriter-random.py
# 暖爪咖啡 · 文案生成器 v2（随机版）
# 新概念：import 模块、列表 list、随机选择 random.choice

import random  # 导入随机模块，相当于请了个帮手

print("=" * 45)
print("  暖爪咖啡 · 文案生成器 v2（随机版）")
print("=" * 45)
print()

product = input("请输入产品名（比如：雪绒热可可）：")
season = input("请输入季节（秋日/冬日/春日/夏日）：")
style = input("请输入风格（治愈/活力/高级）：")
print()

# 根据季节选色调
if season == "秋日":
    color, vibe = "焦糖橙", "温暖醇厚"
elif season == "冬日":
    color, vibe = "雾霾蓝", "治愈暖心"
elif season == "春日":
    color, vibe = "樱花粉", "清新轻快"
else:
    color, vibe = "柠檬黄", "清凉解渴"

# 多套标题模板（列表，用 [] 包起来）
titles_healing = [
    f"把{season}，装进一杯里",
    f"{season}的第一口{product}，慢喝",
    f"一杯{product}，{season}就完整了",
]
titles_energy = [
    f"{season}第一杯{product}，醒了！",
    f"今天的快乐，是{product}给的",
    f"打工人的{season}续命水：{product}",
]
titles_luxury = [
    f"{season}限定 · {product}",
    f"当{season}遇上{product}",
    f"{product} · {season}限时臻选",
]

# 根据风格选列表
if style == "治愈":
    title = random.choice(titles_healing)
elif style == "活力":
    title = random.choice(titles_energy)
else:
    title = random.choice(titles_luxury)

# 随机选一句卖点
selling_points = [
    f"精选当季食材，每一口都是{vibe}",
    f"暖爪独家配方，{product}只在这一季有",
    f"手工慢萃，保留{product}的本味",
    f"一杯{product}，治愈整个{season}",
]
point = random.choice(selling_points)

# 输出
print("=" * 45)
print("  【生成的海报文案】")
print("=" * 45)
print()
print(f"  主标题：{title}")
print(f"  副标题：{season}限定 · {product}")
print(f"  卖点：{point}")
print(f"  建议色调：{color}系")
print()
print("=" * 45)

input("\n按回车键退出...")
