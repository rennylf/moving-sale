"""
小红书发布图生成器 V2
- 列表式布局：每页 4 件物品（2×2 网格）
- 每件：大图 + 类别 + 名称 + 详细描述 + 原价→现价对比
- 装饰元素精简，让物品信息占满画面
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# —— 配置 —— #
W, H = 1080, 1440
OUT_DIR = "/Users/renlingfeng/Library/CloudStorage/OneDrive-个人/Cherry Studio/二手出售/xiaohongshu"
IMG_DIR = "/Users/renlingfeng/Library/CloudStorage/OneDrive-个人/Cherry Studio/二手出售/images"
os.makedirs(OUT_DIR, exist_ok=True)

# 调色板（Claude 暖调）
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

def load_font(path, size):
    return ImageFont.truetype(path, size)

# ============================================================
# 物品数据：含原价 + 现价 + 描述（来自 物品信息.xlsx）
# ============================================================
ITEMS = [
    # 家具
    {"name":"床上小桌板","category":"家具","price":20,"original":39,"desc":"可折叠 60×40cm · 床上学习追剧必备","image":"bed-desk.jpg"},
    {"name":"欧普台灯","category":"家具","price":90,"original":125,"desc":"Ra97.4 高显色 · RG0 无蓝光 · 告别宿舍大冷光","image":"desk-lamp.jpg"},
    {"name":"铁皮床头柜","category":"家具","price":20,"original":52,"desc":"带锁抽屉 · 0.5mm 铁皮 · 高 50cm 单门","image":"bedside-cabinet.jpg"},
    {"name":"京东京造 Z5 人体工学椅","category":"家具","price":180,"original":310,"desc":"可调节头枕扶手 · 腰靠可拆 · 久坐办公学习皆宜","image":"chair.jpg"},

    # 家具 + 大件家电
    {"name":"京造人体工学腰靠","category":"家具","price":100,"original":199,"desc":"记忆棉材质 · 适配办公椅 / 汽车座椅","image":"lumbar-pillow.jpg"},
    {"name":"一米七的大冰箱","category":"家电","price":550,"original":964,"desc":"美的 180L 双门 · 风冷无霜 · 两门不串味","image":"fridge.jpg"},
    {"name":"小米米家洗衣机","category":"家电","price":450,"original":822,"desc":"波轮 10 公斤全自动 · 超净洗 · 出租房通用","image":"mi-washer.jpg"},
    {"name":"米家直流变频塔扇 2","category":"家电","price":100,"original":249,"desc":"无叶落地 · 自然风 · 100 挡调节 · 米家 APP","image":"mi-tower-fan.jpg"},

    # 家电 + 数码
    {"name":"米家无雾加湿器 3","category":"家电","price":150,"original":279,"desc":"鼻炎友好 · 空调房必备 · 滤芯自购","image":"mi-humidifier.jpg"},
    {"name":"SANC 显示器","category":"数码","price":300,"original":599,"desc":"24 英寸 2K · 100Hz · 办公娱乐皆可","image":"monitor.jpg"},
    {"name":"小米路由器 AX3000T","category":"数码","price":90,"original":128,"desc":"千兆双频 · 穿墙强 · 5G 智能 · 一碰连 NFC","image":"mi-router.jpg"},
    {"name":"小爱音箱 Play 增强版","category":"数码","price":60,"original":159,"desc":"LED 时钟显示 · 红外遥控 · 米家智能音箱","image":"xiaomi-speaker.jpg"},

    # 数码 2
    {"name":"米家智能体脂秤 S400","category":"数码","price":45,"original":84,"desc":"25 项身体数据 · 双接蓝牙 · 电池供电","image":"mi-scale.jpg"},
    {"name":"美的显示器挂灯","category":"数码","price":60,"original":118,"desc":"护眼 LED · 触控开关 · 宿舍办公通用","image":"monitor-light.jpg"},
    {"name":"排插一组","category":"数码","price":60,"original":120,"desc":"8 口 1 个 + 4 口 3 个 · 一次带走一整套","image":"power-strips.jpg"},
    {"name":"绿联笔记本立式支架","category":"数码","price":40,"original":69,"desc":"铝合金立式 · 散热好 · 适配 MacBook / 联想","image":"laptop-stand-vertical.jpg"},

    # 数码 + 厨房 + 个护
    {"name":"铝合金笔记本支架","category":"数码","price":30,"original":46,"desc":"可折叠可升降 · 散热立式两用","image":"laptop-stand-alu.jpg"},
    {"name":"米家烧水壶","category":"厨房","price":20,"original":59,"desc":"1.5L · 304 不锈钢内胆 · 烧水快","image":"mi-kettle.jpg"},
    {"name":"米家电饭煲","category":"厨房","price":0,"original":None,"desc":"他人赠予 · 一人食管够","image":"mi-cooker.jpg"},
    {"name":"松下负离子男士夹板","category":"个护","price":90,"original":151,"desc":"直卷两用 · 不伤发防烫 · 蓬松造型","image":"curling-iron.jpg"},

    # 健身 + 其他
    {"name":"迪卡侬网球拍","category":"健身","price":100,"original":249,"desc":"碳素材质 CSR5 · 初学者进阶皆适用","image":"tennis-racket.jpg"},
    {"name":"大球无绳跳绳","category":"健身","price":0,"original":24,"desc":"成人计数负重 · 蓝色","image":"jump-rope.jpg"},
    {"name":"品健六角哑铃 2.5kg","category":"健身","price":0,"original":25,"desc":"男士家用 · 包胶 · 力量训练","image":"dumbbell.jpg"},
    {"name":"懒人抹布（2 卷）","category":"其他","price":0,"original":11,"desc":"未用完 · 免费送","image":"lazy-cloth.jpg"},
]

# 微信二维码路径
QR_PATH = os.path.join(IMG_DIR, "wechat-qr.png")

# ============================================================
#  工具函数
# ============================================================
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

def truncate_desc(text, draw, font, max_width):
    """描述自动截断"""
    if text_w(draw, text, font) <= max_width:
        return text
    while text and text_w(draw, text + "...", font) > max_width:
        text = text[:-1]
    return text + "..."

# ============================================================
#  Image 1: 封面（精简）
# ============================================================
def make_cover():
    canvas = new_canvas()
    draw = ImageDraw.Draw(canvas)

    # 装饰小标签（保留唯一的标签）
    rounded_rect(draw, (60, 110, 230, 150), 20, fill=ACCENT_SOFT)
    draw_text(draw, (145, 130), "搬家出闲置", load_font(SANS, 22), ACCENT, anchor='mm')

    # 主标题
    draw_text(draw, (60, 240), "24 件自用好物", load_font(SERIF, 92), INK)
    draw_text(draw, (60, 360), "低价转让 / 免费送", load_font(SERIF, 56), ACCENT)

    # 副说明
    draw_text(draw, (60, 480), "2024.9 后陆续购置 · 使用都不超过 2 年", load_font(SANS, 26), MUTED)
    draw_text(draw, (60, 525), "正常使用无明显损坏 · 可当面验货", load_font(SANS, 26), MUTED)

    # 分隔线
    draw.line([(60, 600), (W-60, 600)], fill=LINE, width=1)

    # 中部 - 4 个物品预览
    preview_items = [
        ("fridge.jpg", "冰箱"),
        ("mi-washer.jpg", "洗衣机"),
        ("chair.jpg", "人体工学椅"),
        ("mi-router.jpg", "路由器"),
    ]
    y0 = 660
    psize = 150
    gap = 30
    total_w = 4*psize + 3*gap
    start_x = (W - total_w) // 2
    for i, (fn, label) in enumerate(preview_items):
        x = start_x + i*(psize+gap)
        try:
            pimg = fit_image(os.path.join(IMG_DIR, fn), (psize, psize))
            mask = Image.new('L', pimg.size, 0)
            mdraw = ImageDraw.Draw(mask)
            mdraw.rounded_rectangle((0, 0, pimg.size[0], pimg.size[1]), 12, fill=255)
            canvas.paste(pimg, (x, y0), mask)
        except:
            rounded_rect(draw, (x, y0, x+psize, y0+psize), 12, fill=LINE)
        draw_text(draw, (x+psize//2, y0+psize+22), label, load_font(SANS, 18), MUTED, anchor='mt')

    # 关键信息条
    draw.line([(60, 1020), (W-60, 1020)], fill=LINE, width=1)

    info = [
        ("自提", "比亚迪东区"),
        ("时间", "工作日 18:00 后"),
        ("微信", "RyanGrant"),
        ("共计", "24 件"),
    ]
    y_info = 1090
    cell_w = (W - 120) // 4
    for i, (label, val) in enumerate(info):
        x = 60 + i*cell_w
        cx = x + cell_w // 2
        draw.ellipse((cx-4, y_info-4, cx+4, y_info+4), fill=ACCENT)
        draw_text(draw, (cx, y_info+45), label, load_font(SANS, 18), MUTED, anchor='mm')
        draw_text(draw, (cx, y_info+90), val, load_font(SANS, 24), INK, anchor='mm')

    canvas.save(os.path.join(OUT_DIR, "01_cover.jpg"), "JPEG", quality=92, optimize=True)
    print("✓ 01_cover.jpg")

# ============================================================
#  Image 2: 索引（精简）
# ============================================================
def make_index():
    canvas = new_canvas()
    draw = ImageDraw.Draw(canvas)

    draw_text(draw, (60, 120), "全部清单", load_font(SERIF, 64), INK)
    draw_text(draw, (60, 210), "24 件分 6 类 · 下滑看每件详情", load_font(SANS, 24), MUTED)

    # 6 个分类卡片 - 3×2 网格
    cards = [
        ("家具", "5 件", "¥20–180", "桌板/台灯/床头柜/椅子/腰靠", ACCENT_SOFT, ACCENT),
        ("家电", "4 件", "¥100–550", "冰箱/洗衣机/塔扇/加湿器", ACCENT_SOFT, ACCENT),
        ("数码", "8 件", "¥30–300", "显示器/路由器/音箱/挂灯…", ACCENT_SOFT, ACCENT),
        ("厨房", "2 件", "¥20 / 免费", "烧水壶/电饭煲", ACCENT_SOFT, ACCENT),
        ("个护", "1 件", "¥90", "松下夹板", ACCENT_SOFT, ACCENT),
        ("健身 + 其他", "4 件", "¥100 / 4 件免费", "网球拍/跳绳/哑铃/抹布", FREE_SOFT, FREE),
    ]

    y0 = 290
    cw, ch = 320, 320
    gap = 30
    for idx, (name, count, price, items, bg, accent) in enumerate(cards):
        col = idx % 3
        row = idx // 3
        x = 60 + col * (cw + gap)
        y = y0 + row * (ch + gap)

        # 卡片背景
        rounded_rect(draw, (x, y, x+cw, y+ch), 16, fill=CARD, outline=LINE)

        # 顶部圆点
        draw.ellipse((x+30, y+35, x+50, y+55), fill=accent)
        # 名称
        draw_text(draw, (x+65, y+45), name, load_font(SERIF, 32), INK, anchor='lm')
        # 数量 + 价格
        draw_text(draw, (x+30, y+120), f"{count}  ·  {price}", load_font(SANS, 18), MUTED)
        # 物品列表
        items_lines = items.split("/")
        for i, line in enumerate(items_lines):
            draw_text(draw, (x+30, y+170+i*30), "· " + line, load_font(SANS_L, 18), MUTED)

    # 底部信息
    draw.line([(60, 970), (W-60, 970)], fill=LINE, width=1)
    draw_text(draw, (60, 1010), "原价 → 现价", load_font(SERIF, 32), ACCENT)
    draw_text(draw, (60, 1070), "大部分物品 2-5 折转让 · 4 件免费送", load_font(SANS, 22), MUTED)

    info = [
        ("自提", "比亚迪东区宿舍"),
        ("时间", "工作日 18:00 后"),
    ]
    for i, (label, val) in enumerate(info):
        y = 1160 + i*60
        draw.ellipse((60, y, 70, y+10), fill=ACCENT)
        draw_text(draw, (85, y+5), label, load_font(SANS, 22), MUTED, anchor='lm')
        draw_text(draw, (220, y+5), val, load_font(SANS, 22), INK, anchor='lm')

    canvas.save(os.path.join(OUT_DIR, "02_index.jpg"), "JPEG", quality=92, optimize=True)
    print("✓ 02_index.jpg")

# ============================================================
#  Image 3-8: 明细页（每页 4 件）
#  重点：每件物品完整信息：大图 + 类别 + 名称 + 描述 + 价格对比
# ============================================================
def make_item_page(page_num, title, items, hint=""):
    canvas = new_canvas()
    draw = ImageDraw.Draw(canvas)

    # 顶部标题区（精简）
    draw_text(draw, (60, 80), title, load_font(SERIF, 48), INK)
    draw_text(draw, (W-60, 90), f"共 {len(items)} 件", load_font(SANS, 22), MUTED, anchor='ra')
    # 细线分隔
    draw.line([(60, 145), (W-60, 145)], fill=LINE, width=1)

    # 2×2 网格
    cell_w, cell_h = 480, 575
    gap = 25
    x0 = 60
    y0 = 175

    for idx, item in enumerate(items[:4]):
        col = idx % 2
        row = idx // 2
        x = x0 + col * (cell_w + gap)
        y = y0 + row * (cell_h + gap)

        # 卡片背景
        rounded_rect(draw, (x, y, x+cell_w, y+cell_h), 16, fill=CARD, outline=LINE)

        # 图片区（占卡片 55%）
        photo_box = (x+24, y+24, x+cell_w-24, y+340)
        pw, ph = photo_box[2]-photo_box[0], photo_box[3]-photo_box[1]
        try:
            pimg = fit_image(os.path.join(IMG_DIR, item["image"]), (pw, ph))
            mask = Image.new('L', pimg.size, 0)
            mdraw = ImageDraw.Draw(mask)
            mdraw.rounded_rectangle((0, 0, pimg.size[0], pimg.size[1]), 12, fill=255)
            canvas.paste(pimg, photo_box[:2], mask)
        except Exception as e:
            print(f"  图片加载失败 {item['image']}: {e}")
            rounded_rect(draw, photo_box, 12, fill=LINE)

        # 文字区
        tx = x + 24
        ty = y + 360

        # 类别标签（精简，左上小色块）
        cat_color = FREE if item["price"] == 0 else ACCENT
        cat_bg = FREE_SOFT if item["price"] == 0 else ACCENT_SOFT
        cat_text = item["category"]
        cat_w = text_w(draw, cat_text, load_font(SANS, 17)) + 28
        rounded_rect(draw, (tx, ty, tx+cat_w, ty+32), 12, fill=cat_bg)
        draw_text(draw, (tx+cat_w/2, ty+16), cat_text, load_font(SANS, 17), cat_color, anchor='mm')

        # 名称（大字）
        name = item["name"]
        if len(name) > 14:
            name = name[:13] + "…"
        draw_text(draw, (tx, ty+64), name, load_font(SERIF, 30), INK)

        # 描述（自动换行/截断）
        desc = item["desc"]
        desc_max_w = cell_w - 48
        # 第一行
        desc1 = desc
        if text_w(draw, desc1, load_font(SANS, 19)) > desc_max_w:
            # 截断
            while desc1 and text_w(draw, desc1 + "...", load_font(SANS, 19)) > desc_max_w:
                desc1 = desc1[:-1]
            desc1 = desc1 + "..."
        draw_text(draw, (tx, ty+108), desc1, load_font(SANS, 19), MUTED)

        # 价格对比（关键元素）
        py = ty + 158
        if item["price"] == 0:
            # 免费：仅显示「免费送」
            draw_text(draw, (tx, py+8), "免费送", load_font(SERIF, 38), FREE)
            # 右侧小字原价
            if item.get("original"):
                draw_text(draw, (x+cell_w-24, py+8), f"原价 ¥{item['original']}", load_font(SANS, 18), MUTED, anchor='ra')
        else:
            # 原价（灰色 + 删除线）
            orig_text = f"¥{item['original']}"
            draw_text(draw, (tx, py+8), orig_text, load_font(SANS, 22), MUTED)
            # 删除线
            ow = text_w(draw, orig_text, load_font(SANS, 22))
            draw.line([(tx, py+18), (tx+ow, py+18)], fill=MUTED, width=2)

            # 箭头
            ax = tx + ow + 16
            draw_text(draw, (ax, py+8), "→", load_font(SANS, 22), MUTED)

            # 现价（陶土橙，大字）
            nx = ax + 28
            draw_text(draw, (nx, py+8), f"¥{item['price']}", load_font(SERIF, 36), ACCENT)

            # 折扣标签
            if item.get("original"):
                discount = round(item["price"] / item["original"] * 10, 1)
                dtext = f"{discount} 折"
                dw = text_w(draw, dtext, load_font(SANS, 16)) + 22
                dx = x + cell_w - 24 - dw
                rounded_rect(draw, (dx, py+4, dx+dw, py+34), 12, fill=ACCENT_SOFT)
                draw_text(draw, (dx+dw/2, py+19), dtext, load_font(SANS, 16), ACCENT, anchor='mm')

    # 底部提示（仅在非最后一页显示）
    if hint:
        draw_text(draw, (W//2, H-30), hint, load_font(SANS_L, 18), MUTED, anchor='mm')

    canvas.save(os.path.join(OUT_DIR, f"{page_num:02d}_{title}.jpg"), "JPEG", quality=92, optimize=True)
    print(f"✓ {page_num:02d}_{title}.jpg")

# ============================================================
#  Image 9: 联系方式（精简）
# ============================================================
def make_contact():
    canvas = new_canvas()
    draw = ImageDraw.Draw(canvas)

    # 标题
    draw_text(draw, (60, 110), "想要哪件？", load_font(SERIF, 56), INK)
    draw_text(draw, (60, 190), "扫码加我微信聊～", load_font(SANS, 24), MUTED)

    # 二维码（居中放大）
    qr_size = 540
    qr_x = (W - qr_size) // 2
    qr_y = 260
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
    draw_text(draw, (W//2, wcid_box_y+40), "微信号：RyanGrant", load_font(SERIF, 32), ACCENT, anchor='mm')

    # 底部信息
    y_info = wcid_box_y + 130
    info = [
        ("自提地点", "比亚迪东区宿舍"),
        ("看货时间", "工作日 18:00 后 / 周末全天"),
        ("免费物品", "4 件 · 先到先得"),
    ]
    for i, (label, val) in enumerate(info):
        y = y_info + i*48
        draw.ellipse((200-5, y-5, 200+5, y+5), fill=ACCENT)
        draw_text(draw, (220, y), label, load_font(SANS, 22), MUTED, anchor='lm')
        draw_text(draw, (W-200, y), val, load_font(SANS, 22), INK, anchor='rm')

    canvas.save(os.path.join(OUT_DIR, "09_contact.jpg"), "JPEG", quality=92, optimize=True)
    print("✓ 09_contact.jpg")


# ============================================================
#  主流程
# ============================================================
if __name__ == "__main__":
    # 清空旧的明细页（避免遗留）
    for f in os.listdir(OUT_DIR):
        if f.endswith('.jpg') and not f.startswith(('01_', '02_', '09_')):
            os.remove(os.path.join(OUT_DIR, f))
            print(f"  清理旧文件: {f}")

    make_cover()
    make_index()

    # 每页 4 件，按顺序分页（按类别合理分组）
    pages = [
        (3, "家具", ITEMS[0:4]),
        (4, "家具 + 大件家电", ITEMS[4:8]),
        (5, "家电 + 数码", ITEMS[8:12]),
        (6, "数码", ITEMS[12:16]),
        (7, "生活小物", ITEMS[16:20], "→ 最后一页：联系方式"),
        (8, "运动 + 送送送", ITEMS[20:24], "→ 联系方式在下一页"),
    ]

    for p in pages:
        if len(p) == 4:
            make_item_page(*p)
        else:
            make_item_page(*p)

    make_contact()

    # 列出输出
    print("\n=== 全部生成完毕 ===")
    total_size = 0
    for fn in sorted(os.listdir(OUT_DIR)):
        if fn.endswith('.jpg'):
            sz = os.path.getsize(os.path.join(OUT_DIR, fn)) / 1024
            total_size += sz
            print(f"  {fn}  {sz:.0f}KB")
    print(f"\n共 {total_size/1024:.2f}MB")