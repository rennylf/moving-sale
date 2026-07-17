# 搬家清仓 · 家居好物转让

一个纯静态单页网站，用于展示要转让 / 赠送的二手物品，访客可在线浏览并加微信联系。

## 如何更新内容

只需要改 **`data.js`** 一个文件：

- `CONFIG` 里改标题、微信号、取货地点等全局信息。
- `ITEMS` 数组里增删物品，每件字段说明见文件内注释。
  - `price: 0` 表示免费赠送，会显示绿色「免费送」标签。
  - `status`: `available`(在售) / `reserved`(已预订) / `sold`(已送出，卡片变灰)。

## 添加照片

1. 把照片放进 `images/` 文件夹。
2. 在 `data.js` 对应物品的 `images` 里写路径，例如 `images: ["images/sofa.jpg"]`。
3. 微信二维码命名为 `images/wechat-qr.png` 即可自动显示。

没有照片时会自动显示「待补充照片」占位图，不影响浏览。

## 本地预览

用浏览器直接打开 `index.html` 即可。

## 更新线上网站

改完后运行：

```bash
git add -A
git commit -m "更新物品"
git push
```

约 1 分钟后 GitHub Pages 自动生效。
