# quukk Q(ai) 标志 · 暖色版

2026-10-25，依据用户“小写 a 和小写 i 更容易组合成为 Q”的意见调整。

## 形态

第一眼是 Q，细看为单层 a 的圆碗与倾斜 i。主体右侧保持一段短竖边，圆点和圆头斜杆同轴，形成小写 i；斜杆同时构成 Q 尾部。a 为意象表达，并非完整排印字形。保留原版小写 quukk 矢量字标。

## 配色与文件

- 主色陶土：`#AA603F`；深棕：`#302A25`；暖白：`#FAF7F2`。
- `quukk-logo-warm.svg` / `quukk-symbol-warm.svg`：暖色组合与独立图形。
- `quukk-logo-ai-mono.svg` / `quukk-symbol-ai-mono.svg`：深棕单色。
- `quukk-logo-ai-white.svg` / `quukk-symbol-ai-white.svg`：暖白反白。
- `quukk-logo-white.svg` 为主页页脚使用的反白同版副本；前版已保存在 `quukk-logo-original-white.svg`。
- `favicon.svg` 同步为暖色 Q(ai)，深色浏览器主题自动用浅陶土。
- 全部 SVG 为透明背景几何矢量，不依赖字体。组合标志建议宽度不小于 120px；小尺寸用独立图形。

旧版蓝色素材继续保留，原设计说明见 README-original.md。在线 `brand.html` 展示当前版本并提供下载。

## 生成与矢量化

内置 Image Gen 生成三款概念，见 `ai/concepts.png`。从第一款方向重绘 SVG，并调整圆点、斜杆间距与字标比例。`ai/logo-preview.png` 是实际矢量页面截图；`ai/symbol-reference.png` 是符号截图。首页雕塑根据该符号由内置 Image Gen 重新生成，正式文件为 `dist/assets/quukk-warm-sculpture.jpg`。

概念提示：Q monogram constructed from lowercase single-storey a and lowercase i; a circular bowl as dominant ring, tilted i stem as Q tail, dot inside lower-right counter; one unified mark, flat terracotta #AA603F on warm ivory #FAF7F2, consistent substantial strokes, no uppercase A/I, gradients, textures or mockups.

雕塑编辑提示：保持原有暖光与象牙白陶瓷材质，将 Q 轮廓替换为正式 Q(ai) 符号；保留独立圆点和圆头斜杆，形状以矢量截图为准。

## 验收

- 浏览器检查 16、24、32、48、64px 尺寸及暖白反白版本。
- 1440px 桌面和 390px 手机品牌页均无横向溢出，SVG 全部加载。
- 所有 SVG 通过 XML 解析。主页页头、页脚和首屏雕塑使用同一 Q(ai) 方向。
