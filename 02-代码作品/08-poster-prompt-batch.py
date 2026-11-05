# 08-poster-prompt-batch.py
# 暖爪咖啡 · 批量海报提示词生成器
# 一次输入多个产品，分别生成提示词，并汇总到 CSV 文件。

import csv
import os
import re
from pathlib import Path

from openai import OpenAI


# ---------- 第 1 部分：读取 API 配置 ----------

API_KEY = os.getenv("ARK_API_KEY")
MODEL_NAME = os.getenv("ARK_MODEL")

if not API_KEY:
    raise ValueError(
        "没有读取到 ARK_API_KEY。请先在系统环境变量中配置火山引擎 API Key。"
    )

if not MODEL_NAME:
    raise ValueError(
        "没有读取到 ARK_MODEL。请先在系统环境变量中配置模型名称或推理接入点 ID。"
    )

client = OpenAI(
    api_key=API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)


# ---------- 第 2 部分：获取用户输入 ----------

print("=" * 50)
print("  暖爪咖啡 · 批量海报提示词生成器")
print("=" * 50)
print("多个产品名可以用中文逗号、英文逗号或顿号分隔。")
print()

products_text = input("请输入多个新品名：").strip()
products = [
    item.strip()
    for item in re.split(r"[,，、\n]+", products_text)
    if item.strip()
]

if not products:
    raise ValueError("没有输入有效的产品名称，请重新运行程序。")

season = input("请输入季节（秋日/冬日/春日/夏日）：").strip()
color = input("请指定主色调：").strip()
style = input("请输入风格（高级感/极简风）：").strip()


# ---------- 第 3 部分：准备保存位置 ----------

output_dir = Path("批量生成结果")
output_dir.mkdir(parents=True, exist_ok=True)

csv_path = output_dir / "提示词生成汇总.csv"
rows = []


# ---------- 第 4 部分：逐个产品调用 API ----------

for index, product in enumerate(products, start=1):
    print()
    print(f"[{index}/{len(products)}] 正在生成：{product}")

    prompt = f"""你是一个 AI 绘图提示词专家。请为咖啡品牌「暖爪咖啡 WARM PAW」撰写一份可直接用于即梦等 AI 绘图工具的商业海报提示词，并生成三组小红书宣传文案。

产品信息：
- 产品：{product}
- 季节：{season}限定
- 主色调：{color}
- 视觉风格：{style}
- 画面比例：3:4 竖版商业海报
- 品牌角色：Q版小熊猫吉祥物，橘红色毛发、白色面部斑纹、深棕色环纹大尾巴、圆润粗描边
- 品牌视觉：精品咖啡品牌，商业产品摄影与可爱插画融合
- 提示词必须包含：产品主体描述、场景与道具、视觉风格、色彩搭配、品牌角色位置、构图与排版要求
- 提示词要具体、完整，可以直接复制到 AI 绘图工具中使用

请严格按以下结构输出：
【海报生成提示词】
输出一段完整详细的绘图提示词，不要解释创作过程。

【小红书文案】
生成 3 组文案。每组包含：主标题、副标题、品牌 slogan、3 个卖点关键词。
各组之间清楚分隔，内容简洁，突出产品和季节特色。
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是专业的 AI 绘图提示词工程师和咖啡品牌文案专家，"
                        "擅长精品咖啡品牌视觉与商业宣传文案。"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )

        result = response.choices[0].message.content or ""
        if not result.strip():
            raise ValueError("模型返回了空内容。")

        # 清理产品名，避免产品名中的特殊字符影响文件名。
        safe_product = re.sub(r'[\\/:*?"<>|]', "_", product)
        txt_path = output_dir / f"提示词-{safe_product}.txt"
        txt_path.write_text(result, encoding="utf-8")

        rows.append(
            {
                "产品名称": product,
                "季节": season,
                "主色调": color,
                "风格": style,
                "生成状态": "成功",
                "结果文件": txt_path.name,
                "生成内容": result,
            }
        )

        print(f"已保存：{txt_path}")

    except Exception as error:
        # 单个产品失败时，记录错误并继续处理后面的产品。
        error_message = f"{type(error).__name__}: {error}"
        rows.append(
            {
                "产品名称": product,
                "季节": season,
                "主色调": color,
                "风格": style,
                "生成状态": "失败",
                "结果文件": "",
                "生成内容": error_message,
            }
        )
        print(f"生成失败：{error_message}")


# ---------- 第 5 部分：写入 CSV 汇总表 ----------

fieldnames = [
    "产品名称",
    "季节",
    "主色调",
    "风格",
    "生成状态",
    "结果文件",
    "生成内容",
]

with csv_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

success_count = sum(1 for row in rows if row["生成状态"] == "成功")
failure_count = len(rows) - success_count

print()
print("=" * 50)
print("批量任务完成")
print(f"产品总数：{len(products)}")
print(f"成功：{success_count}")
print(f"失败：{failure_count}")
print(f"结果文件夹：{output_dir.resolve()}")
print(f"CSV 汇总表：{csv_path.resolve()}")
print("=" * 50)

input("按回车键退出...")
