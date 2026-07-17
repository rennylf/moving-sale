// ============================================================
//  编辑区：以后你只需要改这个文件就能更新网站内容
// ============================================================

// —— 全局信息 —— //
const CONFIG = {
  title: "搬家清仓 · 家居好物转让",
  subtitle: "因跨省工作调动，家中好物低价转让 / 免费赠送，诚意出，先到先得",
  wechat: "your_wechat_id",              // ← 改成你的微信号
  wechatQr: "images/wechat-qr.png",      // ← 把你的微信二维码图片放到 images/ 文件夹，命名 wechat-qr.png
  location: "XX 市 XX 区 XX 小区（自提）", // ← 改成你的大致取货范围
  pickupTime: "工作日晚上 / 周末全天",     // ← 方便看货取货的时间
  note: "所有物品支持当面验货；大件家具需自提，我可协助搬到楼下。免费物品先到先得，恕不预留。"
};

// —— 物品列表 —— //
// 字段说明：
//   name      物品名称
//   category  类别（家具 / 家电 / 厨房 / 收纳 / 数码 / 其他）
//   price     价格数字；填 0 表示免费赠送
//   priceText 可选，覆盖价格显示文字，比如 "面议" "10 元/个"
//   condition 新旧程度，比如 "9 成新，使用 1 年"
//   desc      详细描述（尺寸、瑕疵等）
//   images    图片路径数组，放到 images/ 文件夹里；留空会显示占位图
//   status    available=在售  reserved=已预订  sold=已送出/已售
const ITEMS = [
  { name: "宜家 KLIPPAN 双人布艺沙发", category: "家具", price: 300, condition: "9 成新，使用 1.5 年", desc: "米灰色，可拆洗沙发套。长 180cm，无破损，猫抓痕迹极少。", images: ["images/sofa.jpg"], status: "available" },
  { name: "实木餐桌 + 4 把椅子", category: "家具", price: 450, condition: "8 成新", desc: "橡木色，桌面 120×70cm。有轻微使用痕迹，结构稳固。", images: [], status: "available" },
  { name: "双门冰箱 210L", category: "家电", price: 500, condition: "7 成新，使用 3 年", desc: "海尔，制冷正常，能效标识齐全。搬家前一直在用。", images: [], status: "available" },
  { name: "滚筒洗衣机 8kg", category: "家电", price: 600, condition: "8 成新", desc: "小天鹅变频，带烘干。无故障，附原装进水管。", images: [], status: "reserved" },
  { name: "1.5 匹壁挂空调", category: "家电", price: 700, priceText: "700（含拆机）", condition: "7 成新", desc: "格力，制冷制热正常。价格含师傅上门拆机。", images: [], status: "available" },
  { name: "IKEA 书桌 + 办公椅", category: "家具", price: 200, condition: "9 成新", desc: "白色书桌 100×60cm，人体工学椅一把。", images: [], status: "available" },
  { name: "五斗柜收纳柜", category: "收纳", price: 150, condition: "8 成新", desc: "白色，五层抽屉，滑轨顺畅。", images: [], status: "available" },
  { name: "全身穿衣镜", category: "家具", price: 80, condition: "9 成新", desc: "落地款，实木边框，无划痕。", images: [], status: "available" },
  { name: "微波炉 20L", category: "厨房", price: 100, condition: "8 成新", desc: "美的机械旋钮款，加热正常。", images: [], status: "available" },
  { name: "电饭煲 4L", category: "厨房", price: 60, condition: "8 成新", desc: "苏泊尔，内胆完好，附蒸屉。", images: [], status: "available" },
  { name: "电水壶", category: "厨房", price: 0, condition: "8 成新", desc: "1.7L 不锈钢，烧水快，免费送。", images: [], status: "available" },
  { name: "厨房锅具三件套", category: "厨房", price: 80, condition: "7 成新", desc: "炒锅 + 汤锅 + 平底锅，不粘涂层基本完好。", images: [], status: "available" },
  { name: "餐具 / 碗碟一批", category: "厨房", price: 0, condition: "适用", desc: "碗、盘、杯子若干，打包免费送，需自取。", images: [], status: "available" },
  { name: "台式护眼灯", category: "数码", price: 40, condition: "9 成新", desc: "可调色温，USB 供电。", images: [], status: "available" },
  { name: "无线路由器 AX3000", category: "数码", price: 90, condition: "9 成新", desc: "小米，WiFi6，已恢复出厂设置。", images: [], status: "available" },
  { name: "落地风扇", category: "家电", price: 50, condition: "8 成新", desc: "遥控款，三档风速，静音。", images: [], status: "available" },
  { name: "取暖器 / 小太阳", category: "家电", price: 40, condition: "8 成新", desc: "冬天备用，发热正常。", images: [], status: "available" },
  { name: "衣物挂烫机", category: "家电", price: 60, condition: "9 成新", desc: "手持挂烫两用，出汽稳定。", images: [], status: "available" },
  { name: "折叠晾衣架", category: "收纳", price: 0, condition: "8 成新", desc: "落地双杆款，可折叠，免费送。", images: [], status: "available" },
  { name: "收纳箱一组（4 个）", category: "收纳", price: 40, priceText: "40（4 个）", condition: "8 成新", desc: "带盖塑料整理箱，适合换季衣物。", images: [], status: "available" },
  { name: "地毯 1.4×2m", category: "家居", price: 70, condition: "8 成新", desc: "短绒灰色，已清洗。", images: [], status: "sold" },
  { name: "落地衣帽架", category: "收纳", price: 30, condition: "9 成新", desc: "金属款，稳固不倒。", images: [], status: "available" },
  { name: "绿植若干（含花盆）", category: "其他", price: 0, condition: "健康", desc: "绿萝、多肉等，带盆免费送，欢迎来领。", images: [], status: "available" },
  { name: "书籍杂物一批", category: "其他", price: 0, condition: "适用", desc: "小说 / 工具书 / 杂物，打包免费送。", images: [], status: "available" }
];
