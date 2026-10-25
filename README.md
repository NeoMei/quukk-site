# quukk 公司主页

中文响应式公司主页，以七款真实产品为基础。纯 HTML、CSS、JavaScript，无构建依赖。

## 本地查看

在本目录执行：

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

打开 http://127.0.0.1:4173/ 。正式部署目录为 `dist/`。资源路径相对网站根目录，因此请通过 HTTP 服务器打开。

## 文件

- `dist/index.html`：公司介绍、七款产品与联系入口。
- `dist/styles.css`：完整响应式视觉设计与减少动态效果支持。
- `dist/app.js`：移动导航、工作场景示意、产品推荐、键盘导航。
- `dist/assets/`：五款产品官网提供的品牌图标。
- `design/`：生成的视觉概念及设计验收说明，不随静态站点部署。
- `.openai/hosting.json`：Sites 站点标识与静态部署配置。

站点默认按 Sites 的仅所有者可见方式部署。未绑定 quukk.com，未修改既有产品站点或 DNS。

## 事实与素材来源

2026-10-25 根据用户提供的公开产品页面及前端发布资源核验。产品功能未进行登录后的端到端验收，站点不承诺性能、准确率、服务可用率或跨产品自动集成。

| 产品 | 官方来源 | 主页定位 |
| --- | --- | --- |
| SuperWagie | https://superwagie.quukk.com/ | 本地 AI 办公与编程智能体 |
| AgentWiki | https://agentwiki.quukk.com/ | 多 Agent 协作的共同大脑 |
| LLMRouter | https://llmrouter.quukk.com/ | 统一 AI API 网关与管理平台 |
| UniHub | https://unihub.quukk.com/ | 统一身份与账户中心 |
| 璇玑 | http://113.249.120.24:3001/cuiqiang/issues | 人类与智能体项目协作 |
| 虾说 | https://newsradar.dreamdt.cn/claw-web/ | 多 AI 智能体讨论 |
| 灵犀知识库 | https://newsradar.dreamdt.cn/lingxi/ | 文档检索与知识问答 |

联系邮箱 `xuefeng.mei@quukk.com` 来自 LLMRouter 公开联系配置。璇玑入口保留用户原始 HTTP 地址。

品牌图标直接来自各产品官方静态资源，沿用品牌标识；没有使用图库照片、第三方人物或客户背书。璇玑和灵犀使用文字标识，以避免把上游/默认 favicon 当成品牌。两处 SuperWagie 工作台为明确标注的场景示意，非真实截图，也不会在主页中调用 AI 或执行任务。

## 交互与检查

- 七款产品入口与外链安全属性。
- 四个应用场景，支持鼠标、触摸、方向键、Home/End。
- 三个工作示意提示，点击切换。
- 手机菜单展开、点击跳转后收起、Escape 关闭。
- 1440、768、390 像素完整页面截图检查；IAB 实测交互与 390 像素无横向溢出。
- 无后端表单、无跟踪代码、无第三方脚本运行时依赖。

详细设计与验收见 `design/REVIEW.md`。
