// ============================================================
//  编辑区：以后你只需要改这个文件就能更新网站内容
// ============================================================

// —— 全局信息 —— //
const CONFIG = {
  title: "搬家出闲置 🌿 坪山 / 比亚迪",
  subtitle: "因工作变动，自用的一些家居好物低价出 / 免费送 ✨",
  purchaseNote: "🌿 绝大部分是 2024.9 后入住比亚迪东区宿舍后置办的，使用时长都不超过 2 年 · 物品均为正常使用、无明显损坏，可以当面验货。",
  wechat: "RyanGrant",                                          // 你的微信号
  wechatQr: "images/wechat-qr.png",                             // 微信二维码（PNG，不参与美化）
  location: "比亚迪东区宿舍（自提）",                            // 取货地点
  pickupTime: "工作日 18:00 后 / 周末全天",                      // 看货取货时间
  note: "🌷 优先面向比亚迪东区宿舍 & 坪山周边的朋友，自提方便；大件可协助搬到楼下。"
};

// —— 物品列表 —— //
// 字段说明：
//   name      物品名称
//   category  类别（家具 / 家电 / 厨房 / 数码 / 健身 / 个护 / 其他）
//   price     价格数字；填 0 或 "免费" 表示免费赠送
//   priceText 可选，覆盖价格显示文字
//   desc      详细描述（尺寸/瑕疵/亮点）
//   images    图片路径数组；留空显示占位图
//   status    available=在售  reserved=已预订  sold=已送出/已售
const ITEMS = [
  { name: "一米七的大冰箱", category: "家电", price: 550, condition: "",
    desc: "美的 180L 双门冰箱，白色，风冷无霜，两门不串味，租房不占地。",
    images: ["images/fridge.jpg"], status: "available" },
  { name: "懒人抹布（2 卷）", category: "其他", price: 0, condition: "",
    desc: "未用完，免费送。",
    images: ["images/lazy-cloth.jpg"], status: "available" },
  { name: "大球无绳跳绳", category: "健身", price: 0, condition: "",
    desc: "成人计数负重减肥，蓝色。",
    images: ["images/jump-rope.jpg"], status: "available" },
  { name: "哑铃", category: "健身", price: 0, condition: "",
    desc: "品健男士家用六角哑铃，包胶，2.5kg。",
    images: ["images/dumbbell.jpg"], status: "available" },
  { name: "小爱音箱", category: "数码", price: 60, condition: "",
    desc: "小米 小爱音箱 Play 增强版，LED 时钟显示，红外遥控，黑色。",
    images: ["images/xiaomi-speaker.jpg"], status: "sold" },
  { name: "小米体脂秤", category: "数码", price: 45, condition: "",
    desc: "米家智能体脂秤 S400，白色，双接蓝牙，25 项身体数据，电池供电。",
    images: ["images/mi-scale.jpg"], status: "sold" },
  { name: "小米路由器", category: "数码", price: 90, condition: "",
    desc: "小米 AX3000T，千兆双频，穿墙强，5G 智能，一碰连 NFC。",
    images: ["images/mi-router.jpg"], status: "available" },
  { name: "床上小桌板", category: "家具", price: 20, condition: "",
    desc: "可折叠，60×40cm，适合床上学习、追剧、用电脑。",
    images: ["images/bed-desk.jpg"], status: "available" },
  { name: "排插一组", category: "数码", price: 60, condition: "",
    desc: "8 口 1 个 + 4 口 3 个，一次带走一整套。",
    images: ["images/power-strips.jpg"], status: "sold" },
  { name: "显示器", category: "数码", price: 300, condition: "",
    desc: "SANC 24 英寸 2K，100Hz，办公娱乐皆可。",
    images: ["images/monitor.jpg"], status: "available" },
  { name: "美的电脑显示器挂灯", category: "数码", price: 60, condition: "",
    desc: "屏幕 LED 护眼挂灯，触控开关，宿舍办公都能用。",
    images: ["images/monitor-light.jpg"], status: "available" },
  { name: "欧普台灯", category: "家具", price: 90, condition: "",
    desc: "Ra97.4 高显色，RG0 无蓝光，可调色温、亮度，告别宿舍大冷光。",
    images: ["images/desk-lamp.jpg"], status: "available" },
  { name: "绿联笔记本竖立侧立散热底座", category: "数码", price: 40, condition: "",
    desc: "铝合金立式支架，可调节，适配 MacBook / 联想 / 华为。",
    images: ["images/laptop-stand-vertical.jpg"], status: "available" },
  { name: "米家无雾加湿器 3", category: "家电", price: 150, condition: "",
    desc: "鼻炎友好，空调房必备。滤芯需自购。",
    images: ["images/mi-humidifier.jpg"], status: "available" },
  { name: "米家直流变频塔扇 2", category: "家电", price: 100, condition: "",
    desc: "无叶落地风扇，自然风，100 挡调节，米家 APP 智能控制。",
    images: ["images/mi-tower-fan.jpg"], status: "sold" },
  { name: "小米米家洗衣机", category: "家电", price: 450, condition: "",
    desc: "波轮 10 公斤全自动，超净洗，省水省电，寝室 / 出租房通用。",
    images: ["images/mi-washer.jpg"], status: "available" },
  { name: "米家烧水壶", category: "厨房", price: 20, condition: "",
    desc: "1.5L，304 不锈钢内胆，烧水快。",
    images: ["images/mi-kettle.jpg"], status: "sold" },
  { name: "米家电饭煲", category: "厨房", price: 0, condition: "",
    desc: "他人赠予，一人食管够。",
    images: ["images/mi-cooker.jpg"], status: "sold" },
  { name: "松下（Panasonic）负离子男士夹板", category: "个护", price: 90, condition: "",
    desc: "直卷两用，刘海短发适用，负离子不伤发、防烫蓬松。",
    images: ["images/curling-iron.jpg"], status: "available" },
  { name: "迪卡侬网球拍", category: "健身", price: 100, condition: "",
    desc: "碳素材质，CSR5，初学者 / 进阶皆适用。",
    images: ["images/tennis-racket.jpg"], status: "available" },
  { name: "铁皮床头柜", category: "家具", price: 20, condition: "",
    desc: "带锁抽屉，0.5mm 铁皮，高 50cm，单门。",
    images: ["images/bedside-cabinet.jpg"], status: "available" },
  { name: "铝合金笔记本支架", category: "数码", price: 30, condition: "",
    desc: "可折叠可升降，散热立式两用，适配联想 / Mac / 戴尔。",
    images: ["images/laptop-stand-alu.jpg"], status: "available" },
  { name: "京东京造 Z5 人体工学椅", category: "家具", price: 180, condition: "",
    desc: "可调节头枕与扶手，腰靠可拆，久坐学习办公皆宜。",
    images: ["images/chair.jpg"], status: "sold" },
  { name: "京造人体工学腰靠", category: "家具", price: 100, condition: "",
    desc: "记忆棉材质，可适配办公椅或汽车座椅，固定带可调。",
    images: ["images/lumbar-pillow.jpg"], status: "available" }
];
