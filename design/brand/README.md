# quukk Q(ai) 标志 · 平行缺口定稿

2026-10-25，采用用户选定的第 3 款，按随后要求修正严格对称、底边平齐，并将圆环缺口改为与 i 平行的直线。用户对最终效果表示“这个不错”。

## 形态

第一眼是 Q，细看为单层 a 的圆碗与倾斜 i。圆环开口两侧沿45°轴镜像，圆点和圆头斜杆的中心落在同一轴线上，形成小写 i；斜杆同时构成 Q 尾部。a 为意象表达，并非完整排印字形。保留原版小写 quukk 矢量字标。

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

内置 Image Gen 生成三款概念，见 `ai/concepts.png`。按用户确认的第3款重绘 SVG，并精确调整圆点、斜杆与镜像开口。当前实际矢量预览位于 `parallel-cut/logo-preview.png`，符号截图为 `parallel-cut/symbol-reference.png`；`ai/` 保留上一版记录。首页雕塑根据该符号由内置 Image Gen 重新生成，正式文件为 `dist/assets/quukk-warm-sculpture.jpg`。

概念提示：Q monogram constructed from lowercase single-storey a and lowercase i; a circular bowl as dominant ring, tilted i stem as Q tail, dot inside lower-right counter; one unified mark, flat terracotta #AA603F on warm ivory #FAF7F2, consistent substantial strokes, no uppercase A/I, gradients, textures or mockups.

雕塑编辑提示：保持原有暖光与象牙白陶瓷材质，将 Q 轮廓替换为正式 Q(ai) 符号；保留独立圆点和圆头斜杆，形状以矢量截图为准。

## 验收

- 浏览器检查 16、24、32、48、64px 尺寸及暖白反白版本。
- 1440px 桌面和 390px 手机品牌页均无横向溢出，SVG 全部加载。
- 所有 SVG 通过 XML 解析。主页页头、页脚和首屏雕塑使用同一 Q(ai) 方向。

## 定稿几何约束

- 标志坐标系224×224，圆心(112,112)，外半径96、内半径60。
- 对称轴为 x=y，所有内外圆开口端点成镜像对，缺口边线为 x−y=±25√2，均平行于 i 的中心线；圆点中心(133,133)，尾杆中心线(163,163)→(191,191)。
- 外圆最低点112+96=208；尾杆圆帽最低点191+17=208，基线差0。由于镜像对称，右侧边界也同为208。
- `parallel-cut/geometry.json` 保留可核验坐标。SVG为几何定稿；首页陶瓷雕塑是依据该稿生成的品牌演绎。
- 最终雕塑提示：使用正式图形轮廓，严格45°对称，圆环缺口直线与i杆平行，两侧净空相等；圆环与i杆底边同一水平基线；正面视角、象牙白陶瓷、暖光、无文字。由内置Image Gen生成。

- 平行缺口定稿：两侧边线斜率均为1，与i轴相同；缺口半宽25、i半宽17，两侧垂直净空均为8。
