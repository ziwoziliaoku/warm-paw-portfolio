# make-portfolio.py
# 暖爪咖啡 WARM PAW · 品牌视觉作品集 PDF 生成器
#
# 用法：
#   python make-portfolio.py
# 输出：
#   同目录下的「暖爪咖啡-作品集.pdf」
#
# 设计说明：
#   - A4 竖版（595 x 842pt）
#   - 品牌色：深棕 #2E211B / 米白 #F7F3EC / 雾霾蓝 #7A95AE / 焦糖 #C08A5A
#   - 字体：微软雅黑（常规 + 粗体）
#   - 图片先压缩到最长边 1600px 再嵌入，避免 PDF 过大

import tempfile
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

BASE = Path(__file__).resolve().parent
ART = BASE / "01-视觉作品"
OUTPUT = BASE / "暖爪咖啡-作品集.pdf"

W, H = A4  # 595.28 x 841.89

# ---------- 品牌色 ----------
INK = HexColor("#2E211B")      # 深棕
CREAM = HexColor("#F7F3EC")    # 米白
BLUE = HexColor("#7A95AE")     # 雾霾蓝
CARAMEL = HexColor("#C08A5A")  # 焦糖
GREY = HexColor("#8A8078")     # 灰

# ---------- 字体 ----------
FONT_DIR = Path(r"C:\Windows\Fonts")
pdfmetrics.registerFont(TTFont("MSYH", str(FONT_DIR / "msyh.ttc"), subfontIndex=0))
pdfmetrics.registerFont(TTFont("MSYH-B", str(FONT_DIR / "msyhbd.ttc"), subfontIndex=0))

MARGIN = 56
CONTENT_W = W - MARGIN * 2


# ========== 工具函数 ==========

def prep_image(path: Path, max_side: int = 1600) -> str:
    """把 PNG 转成压缩后的 JPEG，避免 PDF 体积过大。"""
    with Image.open(path) as im:
        im = im.convert("RGB")
        w, h = im.size
        if max(w, h) > max_side:
            scale = max_side / max(w, h)
            im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        tmp = Path(tempfile.gettempdir()) / f"pf_{abs(hash(path.name)) % 100000}.jpg"
        im.save(tmp, "JPEG", quality=88)
    return str(tmp)


def full_bg(c, color):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def contain(c, img_path: str, x, y, box_w, box_h, border=False):
    """等比缩放图片，居中放进指定框。"""
    with Image.open(img_path) as im:
        iw, ih = im.size
    scale = min(box_w / iw, box_h / ih)
    dw, dh = iw * scale, ih * scale
    dx = x + (box_w - dw) / 2
    dy = y + (box_h - dh) / 2
    c.drawImage(img_path, dx, dy, dw, dh)
    if border:
        c.setStrokeColor(HexColor("#DDD5C8"))
        c.setLineWidth(0.6)
        c.rect(dx, dy, dw, dh, fill=0, stroke=1)


def para(c, lines, x, y, size=10.5, leading=17, color=None, font="MSYH"):
    """逐行写字，返回最后一行的 y。"""
    c.setFillColor(color or INK)
    c.setFont(font, size)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def page_number(c, n, total):
    c.setFillColor(GREY)
    c.setFont("MSYH", 8)
    c.drawRightString(W - MARGIN, 36, f"{n:02d} / {total}")
    c.drawString(MARGIN, 36, "暖爪咖啡 WARM PAW")

    c.setStrokeColor(HexColor("#DDD5C8"))
    c.setLineWidth(0.5)
    c.line(MARGIN, 52, W - MARGIN, 52)


def page_title(c, title, kicker=""):
    c.setFillColor(INK)
    c.setFont("MSYH-B", 19)
    c.drawString(MARGIN, H - 92, title)

    c.setFillColor(CARAMEL)
    c.setFont("MSYH", 8.5)
    c.drawString(MARGIN, H - 110, kicker)

    c.setStrokeColor(HexColor("#DDD5C8"))
    c.setLineWidth(0.6)
    c.line(MARGIN, H - 124, MARGIN + 80, H - 124)


# ========== 页面 ==========

def page_cover(c):
    full_bg(c, INK)

    c.setFillColor(CREAM)
    c.setFont("MSYH", 9)
    c.drawString(MARGIN, H - 64, "PORTFOLIO   /   2026")

    c.setFont("MSYH-B", 44)
    c.drawString(MARGIN, H - 240, "暖爪咖啡")

    c.setFillColor(CARAMEL)
    c.setFont("MSYH", 15)
    c.drawString(MARGIN + 2, H - 276, "W A R M   P A W")

    c.setStrokeColor(CARAMEL)
    c.setLineWidth(0.8)
    c.line(MARGIN, H - 310, MARGIN + 120, H - 310)

    c.setFillColor(CREAM)
    c.setFont("MSYH-B", 15)
    c.drawString(MARGIN, 210, "品牌视觉作品集")
    c.setFont("MSYH", 10)
    c.setFillColor(HexColor("#B9AFA2"))
    c.drawString(MARGIN, 186, "海报  ·  包装物料  ·  IP 角色延展")
    c.drawString(MARGIN, 166, "秋日 / 冬日 两季完整视觉产出")

    c.setFillColor(HexColor("#6E6259"))
    c.setFont("MSYH", 8)
    c.drawString(MARGIN, 60, "WARM PAW  ·  EST. 2026  ·  BEIJING")


def page_intro(c, mascot_img):
    full_bg(c, CREAM)
    page_title(c, "关于品牌", "ABOUT  /  WARM  PAW")

    text_y = H - 176
    para(
        c,
        [
            "暖爪咖啡 WARM PAW 是一个以原创 IP 为核心的",
            "虚拟精品咖啡品牌。品牌角色「小熊猫江天」——",
            "橘红毛发、白色面纹、深棕环纹大尾巴，头戴米白",
            "毛线帽、系红围巾，是品牌的视觉符号与情感入口。",
        ],
        MARGIN,
        text_y,
        size=11,
        leading=21,
    )

    text_y = H - 300
    para(
        c,
        [
            "视觉语言：冬雪治愈 × 极简精品。",
            "冷调雪白与雾霾蓝作基底，暖黄灯光与焦糖棕点缀；",
            "商业产品摄影的质感，加上可爱平涂插画的温度。",
        ],
        MARGIN,
        text_y,
        size=11,
        leading=21,
        color=INK,
    )

    text_y = H - 400
    para(
        c,
        [
            "作品集收录秋、冬两季的完整视觉产出，",
            "涵盖海报、纸杯纸袋包装物料、IP 角色动作延展，",
            "以及配套的小红书文案与海报提示词。",
        ],
        MARGIN,
        text_y,
        size=11,
        leading=21,
        color=GREY,
    )

    # 右侧吉祥物
    contain(c, mascot_img, MARGIN + 250, 130, 250, 250)

    page_number(c, 2, 10)


def page_poster(c, title, kicker, img_path, note_lines, page_no):
    full_bg(c, CREAM)
    page_title(c, title, kicker)

    contain(c, img_path, MARGIN, 190, CONTENT_W, 500)

    para(c, note_lines, MARGIN, 158, size=9.5, leading=15, color=GREY)
    page_number(c, page_no, 10)


def page_packaging(c, title, kicker, img_path, note_lines, page_no):
    full_bg(c, CREAM)
    page_title(c, title, kicker)

    para(c, note_lines, MARGIN, H - 152, size=9.5, leading=15, color=GREY)

    contain(c, img_path, MARGIN, 110, CONTENT_W, 520, border=True)

    page_number(c, page_no, 10)


def page_ip(c, imgs):
    full_bg(c, CREAM)
    page_title(c, "IP 角色延展", "CHARACTER  /  江天")

    para(
        c,
        [
            "同一角色保持形象一致：橘红毛发、白色面部斑纹、",
            "深棕环纹大尾巴、圆润粗描边。通过动作与场景变化，",
            "覆盖日常营业、情感互动、专业拉花三种使用场景。",
        ],
        MARGIN,
        H - 166,
        size=10,
        leading=18,
        color=GREY,
    )

    box = 148
    gap = 22
    total = box * 3 + gap * 2
    start_x = MARGIN + (CONTENT_W - total) / 2
    y = 330

    labels = ["营业 · 端咖啡", "情感 · 捧杯", "专业 · 拉花"]
    for i, img in enumerate(imgs):
        x = start_x + i * (box + gap)
        contain(c, img, x, y, box, box, border=True)
        c.setFillColor(INK)
        c.setFont("MSYH", 9)
        c.drawCentredString(x + box / 2, y - 18, labels[i])

    para(
        c,
        [
            "菜单、贴纸、周边、社媒配图均可复用同一角色形象，",
            "不需要每次重新设定外观，品牌识别度不随物料分散而削弱。",
        ],
        MARGIN,
        262,
        size=9.5,
        leading=16,
        color=GREY,
    )

    page_number(c, 8, 10)


def page_service(c):
    full_bg(c, CREAM)
    page_title(c, "可以为你做什么", "SERVICE")

    items = [
        (
            "01",
            "新品海报",
            "3:4 竖版商业海报，同一产品可出 3 组不同风格方向；",
            "含产品摄影级主体、品牌角色、完整排版层级。",
        ),
        (
            "02",
            "包装物料效果图",
            "纸杯、双杯纸袋、杯套的组合展示板；",
            "正面/背面/侧面多视图，可直接用于提案与打样沟通。",
        ),
        (
            "03",
            "IP 角色动作延展",
            "在统一形象前提下扩展动作与场景，",
            "用于菜单、贴纸、周边、社媒配图。",
        ),
        (
            "04",
            "配套文案",
            "小红书三组文案（主标题 / 副标题 / 口号 / 卖点），",
            "以及可直接投入即梦等工具的海报提示词。",
        ),
    ]

    y = H - 170
    for num, name, line1, line2 in items:
        c.setFillColor(CARAMEL)
        c.setFont("MSYH-B", 11)
        c.drawString(MARGIN, y, num)

        c.setFillColor(INK)
        c.setFont("MSYH-B", 13)
        c.drawString(MARGIN + 34, y, name)

        para(c, [line1, line2], MARGIN + 34, y - 22, size=9.5, leading=15, color=GREY)
        y -= 96

    # 合作流程
    c.setFillColor(INK)
    c.setFont("MSYH-B", 13)
    c.drawString(MARGIN, 232, "合作流程")

    steps = "沟通需求  →  出 2 版方向  →  选定后精修  →  交付源文件"
    c.setFillColor(BLUE)
    c.setFont("MSYH", 10.5)
    c.drawString(MARGIN, 206, steps)

    page_number(c, 9, 10)


def page_back(c):
    full_bg(c, INK)

    c.setFillColor(CREAM)
    c.setFont("MSYH-B", 18)
    c.drawString(MARGIN, H - 300, "把季节，做成故事。")

    c.setStrokeColor(CARAMEL)
    c.setLineWidth(0.8)
    c.line(MARGIN, H - 320, MARGIN + 90, H - 320)

    c.setFillColor(HexColor("#B9AFA2"))
    c.setFont("MSYH", 10)
    c.drawString(MARGIN, H - 360, "如果你也想让新品拥有完整的视觉气质，欢迎联系。")

    c.setFillColor(CREAM)
    c.setFont("MSYH-B", 11)
    c.drawString(MARGIN, 200, "联系方式")

    c.setFillColor(HexColor("#8C8073"))
    c.setFont("MSYH", 10)
    c.drawString(MARGIN, 178, "微信   ：______________________")
    c.drawString(MARGIN, 158, "手机   ：______________________")
    c.drawString(MARGIN, 138, "抖音   ：小熊猫的咖啡屋")

    c.setFillColor(HexColor("#6E6259"))
    c.setFont("MSYH", 8)
    c.drawString(MARGIN, 60, "WARM PAW  ·  PORTFOLIO 2026")


# ========== 主流程 ==========

def main():
    print("准备图片…")
    imgs = {
        "poster_autumn": prep_image(ART / "秋日海报-v2-修正版.png"),
        "poster_winter": prep_image(ART / "冬日海报-v1.png"),
        "poster_minimal": prep_image(ART / "即梦出图-极简雪绒-v1-修复版.png"),
        "pack_autumn": prep_image(ART / "秋日包装展示板-v1.png"),
        "pack_winter": prep_image(ART / "冬日包装展示板-v1.png"),
        "pack_display": prep_image(ART / "包装陈列-v1.png"),
        "mascot1": prep_image(ART / "吉祥物江天-01-端咖啡.png"),
        "mascot2": prep_image(ART / "吉祥物江天-02-捧杯.png"),
        "mascot3": prep_image(ART / "吉祥物江天-03-拉花.png"),
    }
    print(f"  共 {len(imgs)} 张图")

    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("暖爪咖啡 WARM PAW · 品牌视觉作品集")
    c.setAuthor("WARM PAW")
    c.setSubject("品牌视觉作品集：海报 / 包装物料 / IP 角色")

    # 1 封面
    page_cover(c)
    c.showPage()

    # 2 品牌介绍
    page_intro(c, imgs["mascot2"])
    c.showPage()

    # 3-5 海报
    page_poster(
        c,
        "秋日限定海报",
        "POSTER  /  AUTUMN  LIMITED",
        imgs["poster_autumn"],
        [
            "3:4 竖版。产品主体为秋日限定饮品，暖调灯光与落叶元素，",
            "品牌角色位于杯侧不遮挡主体；顶部标题、底部品牌落款分层排版。",
        ],
        3,
    )
    c.showPage()

    page_poster(
        c,
        "冬日限定海报",
        "POSTER  /  WINTER  LIMITED",
        imgs["poster_winter"],
        [
            "3:4 竖版。冷调雪白背景 + 雾霾蓝主色，窗外汇入飘雪与暖光，",
            "热气与奶泡质感为视觉重心，整体保留充足留白。",
        ],
        4,
    )
    c.showPage()

    page_poster(
        c,
        "极简风格海报",
        "POSTER  /  MINIMAL",
        imgs["poster_minimal"],
        [
            "同一产品的另一条视觉路线：纯色雾霾蓝背景、无多余装饰，",
            "靠产品质感与极简排版取胜，适合精品咖啡调性。",
        ],
        5,
    )
    c.showPage()

    # 6-7 包装
    page_packaging(
        c,
        "秋日包装物料",
        "PACKAGING  /  AUTUMN",
        imgs["pack_autumn"],
        [
            "纸杯、双杯纸袋、杯套的组合展示板，正背面分别呈现品牌面与插画面；",
            "标注主要尺寸，可直接用于与供应商沟通打样。",
        ],
        6,
    )
    c.showPage()

    page_packaging(
        c,
        "冬日包装物料",
        "PACKAGING  /  WINTER",
        imgs["pack_winter"],
        [
            "冬日系列沿用冷调雪白与雾霾蓝体系，加入落雪与围巾等季节符号，",
            "包装与海报共用同一套视觉规则，保证线上线下一致。",
        ],
        7,
    )
    c.showPage()

    # 8 IP
    page_ip(c, [imgs["mascot1"], imgs["mascot2"], imgs["mascot3"]])
    c.showPage()

    # 9 服务
    page_service(c)
    c.showPage()

    # 10 封底
    page_back(c)
    c.showPage()

    c.save()

    size_mb = OUTPUT.stat().st_size / (1024 * 1024)
    print()
    print(f"已生成：{OUTPUT}")
    print(f"大小：{size_mb:.1f} MB")


if __name__ == "__main__":
    main()
