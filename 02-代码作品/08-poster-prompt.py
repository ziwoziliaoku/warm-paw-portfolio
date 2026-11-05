# 08-poster-prompt.py
# 暖爪咖啡 · 海报提示词生成器
# 输入产品名，AI 输出一段可以直接复制到即梦的完整提示词

from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

print("=" * 45)
print("  暖爪咖啡 · 海报提示词生成器")
print("=" * 45)
print()

product = input("请输入新品名：")
season = input("请输入季节（秋日/冬日/春日/夏日）：")
color = input("请指定主色调：")
style = input("请输入风格（高级感/极简风）：")
print()
print("AI 正在生成提示词...")
print()

prompt = f"""你是一个 AI 绘图提示词专家。请为咖啡品牌「暖爪咖啡 WARM PAW」写一段即梦/AI 绘图提示词。并且根据产品要求、风格、季节名称生成三组小红书标题。

要求：
- 产品：{product}
- 季节：{season}限定
-主色调：{color}
-风格：{style}
- 尺寸：3:4 竖版商业海报
- 品牌角色：Q版小熊猫吉祥物（橘红毛、白脸纹、深棕环纹大尾巴、粗描边）
- 风格：{style}精品咖啡品牌，商业产品摄影+可爱插画融合
- 包含：产品主体描述、视觉风格、色彩、品牌角色位置、排版要求
- 提示词要完整详细，可以直接复制使用
- 不要输出解释，只输出提示词正文
- 每个标题都为主标题/副标题/品牌slogan为一组，三个卖点关键词，格式简洁
- 小红书标题与提示词空行分辨区分"""


r = client.chat.completions.create(
    model="",
    messages=[
        {"role": "system", "content": "你是专业的 AI 绘图提示词工程师和咖啡品牌文案专家，擅长咖啡品牌视觉。"},
        {"role": "user", "content": prompt}
    ]
)

result = r.choices[0].message.content

print("=" * 45)
print("  【复制下面这段到即梦】")
print("=" * 45)
print()
print(result)
print()
print("=" * 45)

# 保存到文件
with open(f"提示词-{product}.txt", "w", encoding="utf-8") as f:
    f.write(result)
print(f"已保存到：提示词-{product}.txt")

input("\n按回车键退出...")