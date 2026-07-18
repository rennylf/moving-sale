"""
小红书发布图生成器
- 9 张图，3:4 比例 1080×1440
- 视觉与网站 Claude 风格一致
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# —— 配置 —— #
W, H = 1080, 1440
OUT_DIR = "/Users/renlingfeng/Library/CloudStorage/OneDrive-个人/Cherry Studio/二手出售/xiaohongshu"
IMG_DIR = "/Users/renlingfeng/Library/CloudStorage/OneDrive-个人/Cherry Studio/二手出售/images"
os.makedirs(OUT_DIR, exist_ok=True)

# 调色板
BG = (250, 249, 245)
CARD = (255, 255, 255)
INK = (31, 31, 31)
MUTED = (138, 133, 124)
LINE = (232, 230, 224)
ACCENT = (201, 100, 66)
ACCENT_SOFT = (245, 227, 218)
FREE = (90, 143, 107)
FREE_SOFT = (228, 236, 230)

# 字体
SERIF = '/System/Library/Fonts/Supplemental/Songti.ttc'
SANS = '/System/Library/Fonts/STHeiti Medium.ttc'
SANS_L = '/System/Library/Fonts/STHeiti Light.ttc'

def f(path, size):
    return ImageFont.truetype(path, size)

# 物品数据（从 data.js 同步）
ITEMS = [
    # (name, category, price, image_filename, status)
    ("一米七的大冰箱", "家电", 550, "fridge.jpg"),
    ("懒人抹布（2 卷）", "其他", 0, "lazy-cloth.jpg"),
    ("大球无绳跳绳", "健身", 0, "jump-rope.jpg"),
    ("哑铃", "健身", 0, "dumbbell.jpg"),
    ("小爱音箱", "数码", 60, "xiaomi-speaker.jpg"),
    ("小米体脂秤", "数码", 45, "mi-scale.jpg"),
    ("小米路由器", "数码", 90, "mi-router.jpg"),
    ("床上小桌板", "家具", 20, "bed-desk.jpg"),
    ("排插一组", "数码", 60, "power-strips.jpg"),
    ("显示器", "数码", 300, "monitor.jpg"),
    ("美的显示器挂灯", "数码", 60, "monitor-light.jpg"),
    ("欧普台灯", "家具", 90, "desk-lamp.jpg"),
    ("绿联笔记本竖立支架", "数码", 40, "laptop-stand-vertical.jpg"),
    ("米家无雾加湿器 3", "家电", 150, "mi-humidifier.jpg"),
    ("米家直流变频塔扇 2", "家电", 100, "mi-tower-fan.jpg"),
    ("小米米家洗衣机", "家电", 450, "mi-washer.jpg"),
    ("米家烧水壶", "厨房", 20, "mi-kettle.jpg"),
    ("米家电饭煲", "厨房", 0, "mi-cooker.jpg"),
    ("松下负离子夹板", "个护", 90, "curling-iron.jpg"),
    ("迪卡侬网球拍", "健身", 100, "tennis-racket.jpg"),
    ("铁皮床头柜", "家具", 20, "bedside-cabinet.jpg"),
    ("铝合金笔记本支架", "数码", 30, "laptop-stand-alu.jpg"),
    ("京东京造 Z5 人体工学椅", "家具", 180, "chair.jpg"),
    ("京造人体工学腰靠", "家具", 100, "lumbar-pillow.jpg"),
]

# 微信二维码路径
QR_PATH = os.path.join(IMG_DIR, "wechat-qr.png")

# —— 工具函数 —— #
def new_canvas(bg=BG):
    return Image.new('RGB', (W, H), bg)

def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_text(draw, xy, text, font, color=INK, anchor='la'):
    draw.text(xy, text, font=font, fill=color, anchor=anchor)

def text_w(draw, text, font):
    bbox = draw.textbbox((0,0), text, font=font)
    return bbox[2] - bbox[0]

def fit_image(path, size, mode='cover'):
    """mode: cover=裁剪填满, contain=完整显示"""
    img = Image.open(path).convert('RGB')
    tw, th = size
    iw, ih = img.size
    if mode == 'cover':
        scale = max(tw/iw, th/ih)
        nw, nh = int(iw*scale), int(ih*scale)
        img = img.resize((nw, nh), Image.LANCZOS)
        x = (nw - tw) // 2
        y = (nh - th) // 2
        return img.crop((x, y, x+tw, y+th))
    else:
        scale = min(tw/iw, th/ih)
        nw, nh = int(iw*scale), int(ih*scale)
        img = img.resize((nw, nh), Image.LANCZOS)
        canvas = Image.new('RGB', size, BG)
        canvas.paste(img, ((tw-nw)//2, (th-nh)//2))
        return canvas

# 价格文字
def price_text(price):
    if price == 0: return "免费"
    return f"¥{price}"

# 类别标签（用纯文字，无 emoji）
CAT_LABEL = {
    "家具": "家具",
    "家电": "家电",
    "数码": "数码",
    "厨房": "厨房",
    "健身": "运动",
    "个护": "个护",
    "其他": "其他",
}

# ============================================================
#  Image 1: 封面
# ============================================================
def make_cover():
    canvas = new_canvas()
    draw = ImageDraw.Draw(canvas)

    # 顶部细线
    draw.line([(60, 110), (W-60, 110)], fill=LINE, width=1)

    # 顶部小标识
    draw_text(draw, (60, 80), "XIAOHONGSHU · 搬家季", f(SANS_L, 18), MUTED)
    draw_text(draw, (W-60, 80), "01 / 09", f(SANS, 18), MUTED, anchor='ra')

    # 装饰小标签
    rounded_rect(draw, (60, 160, 240, 200), 20, fill=ACCENT_SOFT)
    draw_text(draw, (150, 180), "搬家出闲置", f(SANS, 22), ACCENT, anchor='mm')

    # 主标题
    draw_text(draw, (60, 290), "24 件自用好物", f(SERIF, 92), INK)
    draw_text(draw, (60, 400), "低价转让 / 免费送", f(SERIF, 60), ACCENT)

    # 副说明
    draw_text(draw, (60, 510), "2024.9 后陆续购置 · 使用不超过 2 年", f(SANS, 26), MUTED)
    draw_text(draw, (60, 555), "物品均为正常使用 · 可以当面验货", f(SANS, 26), MUTED)

    # 中部分隔线
    draw.line([(60, 620), (W-60, 620)], fill=LINE, width=1)

    # 中部 - 4 个物品预览
    preview_items = [
        ("fridge.jpg", "冰箱"),
        ("mi-washer.jpg", "洗衣机"),
        ("chair.jpg", "人体工学椅"),
        ("mi-router.jpg", "路由器"),
    ]
    y0 = 670
    psize = 140
    gap = 30
    total_w = 4*psize + 3*gap
    start_x = (W - total_w) // 2
    for i, (fn, label) in enumerate(preview_items):
        x = start_x + i*(psize+gap)
        try:
            pimg = fit_image(os.path.join(IMG_DIR, fn), (psize, psize))
            canvas.paste(pimg, (x, y0))
        except:
            rounded_rect(draw, (x, y0, x+psize, y0+psize), 12, fill=LINE)
        # 标签
        draw_text(draw, (x+psize//2, y0+psize+20), label, f(SANS, 18), MUTED, anchor='mt')

    # 下部分隔
    draw.line([(60, 1010), (W-60, 1010)], fill=LINE, width=1)

    # 底部信息条 - 4 列
    info = [
        ("自提地点", "比亚迪东区"),
        ("看货时间", "工作日 18 点后"),
        ("联系方式", "微信 RyanGrant"),
        ("物品件数", "24 件"),
    ]
    y_info = 1080
    cell_w = (W - 120) // 4
    for i, (label, val) in enumerate(info):
        x = 60 + i*cell_w
        cx = x + cell_w // 2
        # 顶部小圆点装饰
        draw.ellipse((cx-4, y_info-4, cx+4, y_info+4), fill=ACCENT)
        draw_text(draw, (cx, y_info+50), label, f(SANS, 18), MUTED, anchor='mm')
        draw_text(draw, (cx, y_info+92), val, f(SANS, 22), INK, anchor='mm')

    canvas.save(os.path.join(OUT_DIR, "01_cover.jpg"), "JPEG", quality=92, optimize=True)
    print("✓ 01_cover.jpg")

# ============================================================
#  Image 2: 总览索引
# ============================================================
def make_index():
    canvas = new_canvas()
    draw = ImageDraw.Draw(canvas)

    # 顶部
    draw.line([(60, 110), (W-60, 110)], fill=LINE, width=1)
    draw_text(draw, (60, 80), "XIAOHONGSHU · 全部清单", f(SANS_L, 18), MUTED)
    draw_text(draw, (W-60, 80), "02 / 09", f(SANS, 18), MUTED, anchor='ra')

    # 标题
    draw_text(draw, (60, 170), "24 件分 6 类", f(SERIF, 64), INK)
    draw_text(draw, (60, 260), "按住图片下滑看明细 · 每页 4 件", f(SANS, 22), MUTED)

    # 4 个分类卡片 - 2x2 网格
    cards = [
        ("家具", "5 件", "¥20-180", [
            "床上小桌板 / 欧普台灯", "铁皮床头柜 / 人体工学椅", "人体工学腰靠"
        ], ACCENT_SOFT, ACCENT),
        ("家电", "4 件", "¥100-550", [
            "大冰箱 / 洗衣机", "塔扇 / 加湿器"
        ], ACCENT_SOFT, ACCENT),
        ("数码", "8 件", "¥30-300", [
            "显示器 / 路由器 / 音箱", "体脂秤 / 排插 / 挂灯", "笔记本支架 ×2"
        ], ACCENT_SOFT, ACCENT),
        ("生活", "7 件", "免费-100", [
            "烧水壶 / 夹板 / 网球拍", "+ 4 件免费送", "抹布 / 跳绳 / 哑铃 / 电饭煲"
        ], FREE_SOFT, FREE),
    ]

    y0 = 340
    cw, ch = 480, 260
    gap = 30
    for idx, (name, count, price_range, lines, bg, accent) in enumerate(cards):
        col = idx % 2
        row = idx // 2
        x = 60 + col * (cw + gap)
        y = y0 + row * (ch + gap)

        # 卡片背景
        rounded_rect(draw, (x, y, x+cw, y+ch), 16, fill=CARD, outline=LINE)

        # 顶部圆点装饰
        draw.ellipse((x+30, y+38, x+50, y+58), fill=accent)
        # 名称
        draw_text(draw, (x+65, y+48), name, f(SERIF, 36), INK, anchor='lm')
        # 数量 + 价格
        draw_text(draw, (x+30, y+155), f"{count}  ·  {price_range}", f(SANS, 18), MUTED)
        # 物品列表
        for i, line in enumerate(lines):
            color = accent if "免费" in line else MUTED
            weight = SANS if "免费" in line else SANS_L
            draw_text(draw, (x+30, y+195+i*22), "· " + line, f(weight, 17), color)

    # 底部提示
    draw_text(draw, (60, H-60), "滑动看每件物品的实物图与详情",
              f(SANS, 18), MUTED)

    canvas.save(os.path.join(OUT_DIR, "02_index.jpg"), "JPEG", quality=92, optimize=True)
    print("✓ 02_index.jpg")

# ============================================================
#  Image 3-8: 物品明细 (2x2 网格)
# ============================================================
def make_item_page(page_num, title, items, hint="滑动看下一类"):
    canvas = new_canvas()
    draw = ImageDraw.Draw(canvas)

    # 顶部
    draw.line([(60, 110), (W-60, 110)], fill=LINE, width=1)
    draw_text(draw, (60, 80), f"XIAOHONGSHU · {title}", f(SANS_L, 18), MUTED)
    draw_text(draw, (W-60, 80), f"{page_num:02d} / 09", f(SANS, 18), MUTED, anchor='ra')

    # 标题
    draw_text(draw, (60, 150), title, f(SERIF, 56), INK)
    draw_text(draw, (60, 220), f"共 {len(items)} 件", f(SANS, 22), MUTED)

    # 2x2 网格
    cell_w, cell_h = 480, 500
    gap = 30
    x0 = 60
    y0 = 290
    for idx, item in enumerate(items[:4]):
        col = idx % 2
        row = idx // 2
        x = x0 + col * (cell_w + gap)
        y = y0 + row * (cell_h + gap)

        # 卡片
        rounded_rect(draw, (x, y, x+cell_w, y+cell_h), 16, fill=CARD, outline=LINE)

        # 图片
        photo_box = (x+30, y+30, x+cell_w-30, y+330)  # 420x300
        try:
            pimg = fit_image(os.path.join(IMG_DIR, item[3]), (photo_box[2]-photo_box[0], photo_box[3]-photo_box[1]))
            # 圆角遮罩
            mask = Image.new('L', pimg.size, 0)
            mdraw = ImageDraw.Draw(mask)
            mdraw.rounded_rectangle((0, 0, pimg.size[0], pimg.size[1]), 12, fill=255)
            canvas.paste(pimg, photo_box[:2], mask)
        except Exception as e:
            print(f"  图片加载失败 {item[3]}: {e}")
            rounded_rect(draw, photo_box, 12, fill=LINE)

        # 类别小标签
        cat_bg = FREE_SOFT if item[1] == "其他" else ACCENT_SOFT
        cat_fg = FREE if item[1] == "其他" else ACCENT
        rounded_rect(draw, (x+30, y+360, x+150, y+395), 14, fill=cat_bg)
        draw_text(draw, (x+90, y+378), CAT_LABEL.get(item[1], item[1]), f(SANS, 17), cat_fg, anchor='mm')

        # 名称
        name = item[0]
        if len(name) > 12:
            name = name[:11] + "…"
        draw_text(draw, (x+30, y+415), name, f(SERIF, 26), INK)

        # 价格 (用 SANS 字体以确保 ¥ 正常显示)
        price_color = FREE if item[2] == 0 else ACCENT
        price_label = price_text(item[2])
        draw_text(draw, (x+30, y+460), price_label, f(SANS, 38), price_color)

    # 底部提示
    draw_text(draw, (60, H-55), hint, f(SANS, 18), MUTED)

    canvas.save(os.path.join(OUT_DIR, f"{page_num:02d}_{title}.jpg"), "JPEG", quality=92, optimize=True)
    print(f"✓ {page_num:02d}_{title}.jpg")

# ============================================================
#  Image 9: 联系方式
# ============================================================
def make_contact():
    canvas = new_canvas()
    draw = ImageDraw.Draw(canvas)

    # 顶部
    draw.line([(60, 110), (W-60, 110)], fill=LINE, width=1)
    draw_text(draw, (60, 80), "XIAOHONGSHU · 联系方式", f(SANS_L, 18), MUTED)
    draw_text(draw, (W-60, 80), "09 / 09", f(SANS, 18), MUTED, anchor='ra')

    # 标题
    draw_text(draw, (60, 170), "想要哪件？", f(SERIF, 56), INK)
    draw_text(draw, (60, 250), "扫码加我微信聊～", f(SANS, 24), MUTED)

    # 二维码（居中放大）
    qr_size = 480
    qr_x = (W - qr_size) // 2
    qr_y = 330
    try:
        qr_img = Image.open(QR_PATH).convert('RGB')
        qr_img.thumbnail((qr_size, qr_size), Image.LANCZOS)
        canvas.paste(qr_img, (qr_x + (qr_size-qr_img.size[0])//2,
                              qr_y + (qr_size-qr_img.size[1])//2))
    except Exception as e:
        print(f"  二维码加载失败: {e}")
        rounded_rect(draw, (qr_x, qr_y, qr_x+qr_size, qr_y+qr_size), 12, fill=LINE)

    # 微信 ID 框
    wcid_box_y = qr_y + qr_size + 50
    rounded_rect(draw, (180, wcid_box_y, W-180, wcid_box_y+80), 16, fill=ACCENT_SOFT)
    draw_text(draw, (W//2, wcid_box_y+40), "微信号：RyanGrant", f(SERIF, 32), ACCENT, anchor='mm')

    # 底部信息
    y_info = wcid_box_y + 130
    info = [
        ("自提地点", "比亚迪东区宿舍"),
        ("看货时间", "工作日 18:00 后 / 周末全天"),
        ("免费物品", "4 件，先到先得"),
    ]
    for i, (label, val) in enumerate(info):
        y = y_info + i*48
        # 圆点装饰
        draw.ellipse((200-5, y-5, 200+5, y+5), fill=ACCENT)
        draw_text(draw, (220, y), label, f(SANS, 22), MUTED, anchor='lm')
        draw_text(draw, (W-200, y), val, f(SANS, 22), INK, anchor='rm')

    # 底部小字
    draw_text(draw, (W//2, H-50), "欢迎随时来取  ·  期待与你见面",
              f(SANS, 18), MUTED, anchor='mm')

    canvas.save(os.path.join(OUT_DIR, "09_contact.jpg"), "JPEG", quality=92, optimize=True)
    print("✓ 09_contact.jpg")


# ============================================================
#  分组
# ============================================================
# 家具
FURN = [
    ("床上小桌板", "家具", 20, "bed-desk.jpg"),
    ("欧普台灯", "家具", 90, "desk-lamp.jpg"),
    ("铁皮床头柜", "家具", 20, "bedside-cabinet.jpg"),
    ("京东京造 Z5 人体工学椅", "家具", 180, "chair.jpg"),
]
# 家具 2 (腰靠 + 床头)
FURN2 = [
    ("京造人体工学腰靠", "家具", 100, "lumbar-pillow.jpg"),
    ("一米七的大冰箱", "家电", 550, "fridge.jpg"),
    ("小米米家洗衣机", "家电", 450, "mi-washer.jpg"),
    ("米家直流变频塔扇 2", "家电", 100, "mi-tower-fan.jpg"),
]
# 家电
APPL = [
    ("米家无雾加湿器 3", "家电", 150, "mi-humidifier.jpg"),
    ("显示器", "数码", 300, "monitor.jpg"),
    ("小米路由器", "数码", 90, "mi-router.jpg"),
    ("小爱音箱", "数码", 60, "xiaomi-speaker.jpg"),
]
# 数码 2
DIGI = [
    ("小米体脂秤", "数码", 45, "mi-scale.jpg"),
    ("美的显示器挂灯", "数码", 60, "monitor-light.jpg"),
    ("排插一组", "数码", 60, "power-strips.jpg"),
    ("绿联笔记本竖立支架", "数码", 40, "laptop-stand-vertical.jpg"),
]
# 数码 3
DIGI2 = [
    ("铝合金笔记本支架", "数码", 30, "laptop-stand-alu.jpg"),
    ("米家烧水壶", "厨房", 20, "mi-kettle.jpg"),
    ("米家电饭煲", "厨房", 0, "mi-cooker.jpg"),
    ("松下负离子夹板", "个护", 90, "curling-iron.jpg"),
]
# 健身 + 其他
SPORT = [
    ("大球无绳跳绳", "健身", 0, "jump-rope.jpg"),
    ("哑铃", "健身", 0, "dumbbell.jpg"),
    ("迪卡侬网球拍", "健身", 100, "tennis-racket.jpg"),
    ("懒人抹布（2 卷）", "其他", 0, "lazy-cloth.jpg"),
]


# ============================================================
#  主流程
# ============================================================
if __name__ == "__main__":
    make_cover()
    make_index()
    make_item_page(3, "家具", FURN)
    make_item_page(4, "腰靠 + 大件家电", FURN2)
    make_item_page(5, "小家电 + 数码", APPL)
    make_item_page(6, "更多数码", DIGI)
    make_item_page(7, "生活小物", DIGI2)
    make_item_page(8, "运动 + 送送送", SPORT, hint="→ 最后一页：联系方式")
    make_contact()

    # 列出输出
    print("\n=== 全部生成完毕 ===")
    for f in sorted(os.listdir(OUT_DIR)):
        if f.endswith('.jpg'):
            sz = os.path.getsize(os.path.join(OUT_DIR, f)) / 1024
            print(f"  {f}  {sz:.0f}KB")
