# 09-copywriter-tool.py
# 暖爪咖啡 · 文案工具 v2（函数化 + 风格模板库 + API 自动重试）
# 从 08 批量版升级：核心逻辑拆成函数；新增 4 种风格预设；网络失败自动重试。

import csv
import os
import re
import time
from pathlib import Path

from openai import OpenAI


# ========== 第 1 部分：API 配置（从环境变量读取） ==========

API_KEY = os.getenv("ARK_API_KEY")
MODEL_NAME = os.getenv("ARK_MODEL")

if not API_KEY:
    raise ValueError("没有读取到 ARK_API_KEY。请先在系统环境变量中配置火山引擎 API Key。")

if not MODEL_NAME:
    raise ValueError("没有读取到 ARK_MODEL。请先在系统环境变量中配置模型名称或推理接入点 ID。")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)


# ========== 第 2 部分：风格模板库（新增，字典） ==========

# 每个风格对应一段「风格描述片段」，会拼进发给 AI 的提示词里。
STYLE_TEMPLATES = {
    "极简风": "极简高级感，纯色干净背景，留白充足，构图克制优雅",
    "治愈系": "暖萌治愈风格，柔和光线，温暖氛围，可爱细节丰富",
    "复古风": "复古质感，低饱和度胶片色调，怀旧咖啡店氛围，颗粒细腻",
    "高级感": "精品商业摄影质感，光影层次丰富，材质细节细腻，杂志级排版",
    "国风": "新中式国潮风格，水墨晕染背景，朱砂红与黛蓝配色，古典雅致",
}

DEFAULT_STYLE = "极简风"  # 输入无效时兜底使用的风格


# ========== 第 3 部分：核心函数 ==========

def build_prompt(product: str, season: str, color: str, style: str) -> str:
    """把产品信息和风格拼成给 AI 的完整提示词。"""
    style_desc = STYLE_TEMPLATES.get(style, style)

    prompt = f"""你是一个 AI 绘图提示词专家。请为咖啡品牌「暖爪咖啡 WARM PAW」撰写一份可直接用于即梦等 AI 绘图工具的商业海报提示词，并生成三组小红书宣传文案。

产品信息：
- 产品：{product}
- 季节：{season}限定
- 主色调：{color}
- 视觉风格：{style_desc}
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
    return prompt


def call_ai(prompt: str, max_retries: int = 2) -> str:
    """调用豆包大模型生成内容；失败自动重试，最多重试 max_retries 次。"""
    system_content = (
        "你是专业的 AI 绘图提示词工程师和咖啡品牌文案专家，"
        "擅长精品咖啡品牌视觉与商业宣传文案。"
    )

    last_error = None
    for attempt in range(1, max_retries + 2):  # 首次 + 重试次数
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": prompt},
                ],
            )
            result = response.choices[0].message.content or ""
            if result.strip():
                return result
            last_error = ValueError("模型返回了空内容。")
        except Exception as error:
            last_error = error

        print(f"  调用失败（第 {attempt} 次），2 秒后重试...")
        time.sleep(2)

    raise last_error


def safe_filename(name: str) -> str:
    """清理文件名中 Windows 不允许的特殊字符。"""
    return re.sub(r'[\\/:*?"<>|]', "_", name)


def save_result(product: str, content: str, output_dir: Path) -> Path:
    """把生成内容保存为 txt 文件，返回文件路径。"""
    txt_path = output_dir / f"提示词-{safe_filename(product)}.txt"
    txt_path.write_text(content, encoding="utf-8")
    return txt_path


def write_csv(rows: list, csv_path: Path) -> None:
    """把汇总记录写入 CSV（带表头）。"""
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


# ========== 第 4 部分：主流程 ==========

def main() -> None:
    print("=" * 50)
    print("  暖爪咖啡 · 文案工具 v2")
    print("=" * 50)
    print("多个产品名可以用中文逗号、英文逗号或顿号分隔。")
    print()

    # 1) 输入产品名
    products_text = input("请输入多个新品名：").strip()
    products = [
        item.strip()
        for item in re.split(r"[,，、\n]+", products_text)
        if item.strip()
    ]
    if not products:
        raise ValueError("没有输入有效的产品名称，请重新运行程序。")

    # 2) 输入季节、主色调
    season = input("请输入季节（秋日/冬日/春日/夏日）：").strip()
    color = input("请指定主色调：").strip()

    # 3) 输入风格：先展示可选风格，输入无效时用默认风格兜底
    print()
    print("可选风格：" + " / ".join(STYLE_TEMPLATES.keys()))
    style = input("请输入风格（可直接回车使用默认）：").strip() or DEFAULT_STYLE
    if style not in STYLE_TEMPLATES:
        print(f"  未识别风格「{style}」，已使用默认风格「{DEFAULT_STYLE}」。")
        style = DEFAULT_STYLE

    # 4) 准备保存位置
    output_dir = Path("批量生成结果")
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "提示词生成汇总.csv"
    rows = []

    # 5) 逐个产品生成
    for index, product in enumerate(products, start=1):
        print()
        print(f"[{index}/{len(products)}] 正在生成：{product}")

        prompt = build_prompt(product, season, color, style)

        try:
            result = call_ai(prompt)
            txt_path = save_result(product, result, output_dir)
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
            print(f"  已保存：{txt_path.name}")
        except Exception as error:
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
            print(f"  生成失败：{error_message}")

    # 6) 写入汇总并打印结果
    write_csv(rows, csv_path)

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


if __name__ == "__main__":
    main()
