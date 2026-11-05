# 04-copywriter.py
# 暖爪咖啡 · 文案生成器 v1
# 功能：输入产品名、季节、风格，自动生成一段海报文案

print("=" * 45)
print("  暖爪咖啡 · 文案生成器 v1")
print("=" * 45)
print()

# 第 1 步：收集用户输入
product = input("请输入产品名（比如：雪绒热可可）：")
season = input("请输入季节（秋日/冬日/春日/夏日）：")
style = input("请输入风格（治愈/活力/高级）：")

print()

# 第 2 步：根据季节选配色和氛围
if season == "秋日":
    main_color = "焦糖橙"
    accent = "暖棕"
    vibe = "温暖醇厚"
elif season == "冬日":
    main_color = "雾霾蓝"
    accent = "雪白"
    vibe = "治愈暖心"
elif season == "春日":
    main_color = "樱花粉"
    accent = "嫩绿"
    vibe = "清新轻快"
else:
    main_color = "柠檬黄"
    accent = "海蓝"
    vibe = "清凉解渴"

# 第 3 步：根据风格选标题模板
if style == "治愈":
    title = f"把{season}，装进一杯里"
    slogan = f"暖一杯{product}，给这个{season}一点温柔"
elif style == "活力":
    title = f"{season}第一杯{product}，醒了！"
    slogan = f"今天的快乐，是{product}给的"
else:  # 高级
    title = f"{season}限定 · {product}"
    slogan = f"甄选当季风味，仅限{season}"

# 第 4 步：组装完整文案
print("=" * 45)
print("  【生成的海报文案】")
print("=" * 45)
print()
print(f"  主标题：{title}")
print(f"  副标题：{season}限定 · {product}")
print(f"  英文标签：{season.upper()} LIMITED")
print(f"  品牌口号：{slogan}")
print(f"  建议色调：{main_color} + {accent}")
print(f"  氛围关键词：{vibe}")
print()
print("=" * 45)

input("\n按回车键退出...")
