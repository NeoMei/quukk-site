# 113 官网部署

## 当前发布

- 正式地址：中文 **https://www.quukk.com/**；英文 **https://www.quukk.com/en/**。
- 发布日期：2026-10-25（Asia/Shanghai）。
- 内容基线：`a9ccd27aa40fb3a280d2005d81e3b2d34a4b025b`；当前版本包含后续产品名称、官网链接、完整中英文切换及产品能力与使用示例版式更新。
- 发布版本：`20261025-product-stories`，只发布 `dist/` 的 37 个静态文件。前一版本 `20261025-bilingual` 及更早版本保留供回滚。
- 服务器：`113.249.120.24`；复用本机已建立的 SSH 连接，未在项目文件中保存密码。
- 发布目录：`/var/www/quukk-company/releases/20261025-product-stories/`。
- 当前目录：`/var/www/quukk-company/current`，符号链接指向上述版本。
- Nginx 配置：`/etc/nginx/sites-available/quukk-company`，启用链接 `/etc/nginx/sites-enabled/zz-quukk-company`。
- 本地配置副本：`nginx-quukk-company.conf`。
- 变更前 Nginx 备份及文件校验清单：`/var/backups/quukk-company/20261025T081500Z-a9ccd27/`。

## 入口与域名

公网 `www.quukk.com:443` → 既有入口 `47.108.85.222` → `113.249.120.24:8484` → 本站 Nginx 虚拟主机。本次未改 DNS、入口服务器、防火墙或既有产品配置。

Google 与 Cloudflare DoH 均确认 `www.quukk.com`、`quukk.com` 的 A 记录为 `47.108.85.222`，无 AAAA/CNAME，TTL 600 秒。带唯一探测参数的公网请求出现在 113 的访问日志中，来源为 47，确认实际转发路径。

此前 `www.quukk.com` 命中默认站点，返回 SuperWagie 页面；新增专属主机后返回本公司的主页。配置文件按 `zz-` 排序，保留既有监听端口的默认站点顺序。

复用服务器已有 `*.quukk.com` 证书，公网验证信任链和域名成功，有效期至 2026-12-15。该证书**不覆盖裸域 `quukk.com`**，因此本次正式地址采用 `www.quukk.com`。没有为裸域申请新证书；裸域 HTTPS 尚未启用。现有证书更新由原维护流程负责，本次没有新增自动续期。

Nginx 的 80/7680 虚拟主机已配置跳转至 HTTPS www，服务器本机测试返回 301。但公网入口 80 当前连接超时，未宣称公网 HTTP 跳转可用。发布地址请使用完整 HTTPS URL。113 公网 80/443 直接探测也未成功，沿用现有入口，不能直接把 DNS 改到 113。

## 验收

- 全部 37 个发布文件在 113 通过 SHA-256 校验。
- 公网 HTTPS 中文首页 200，内容与本地 `dist/index.html` 完全一致；SHA-256：`1f7f1a4c912a6c3600e43c8f9b4fc4734c8e248cbc2355e9d639b02c0576136c`。
- 英文首页 SHA-256：`1a6e7b4cdf6394d41bba2e20c9ced6fd8ba7104c0d0c5331f352034280c644a7`。两套首页、品牌页、语言 JS/CSS 和应用 JS 的公网响应均与本地逐字节一致。
- 五款产品主图、虾说讨论示例、JavaScript 和三个 CSS 均返回 200，类型正确。
- 独立检查确认 SuperWagie、AgentWiki、UniHub、LLMRouter 首页仍返回各自产品内容，未被主站覆盖。
- 浏览器打开正式 HTTPS 域名，标题、导航、产品内容和联系邮箱 `quukk2026@agent.qq.com` 正确；首次上线截图见 `evidence/www-quukk-homepage.jpg`。
- Nginx 配置检查无错误、无警告，平滑 reload 后服务 active。首次 reload 后紧接的请求仍命中旧 worker，随后本机和公网复核均返回新站点。
- 不存在的资源返回 404；静态资源采用 `no-cache` 重新验证，避免稳定文件名导致更新后仍显示旧版本。

## 产品名称更新验收（2026-10-25）

五款应用统一为犇马 SuperWagie、天枢 AgentWiki、璇玑 XuanGene、灵犀 LingXi、虾说 ClawMessenger；犇马官网采用 `https://www.superwagie.com/`，天枢采用 `https://AgentWiki.quukk.com/`。同步首屏索引、产品标题、SEO 描述、无障碍说明、截图弹窗和动态场景推荐。真实产品截图内容保留。

本地 1440 和 390 像素检查无水平溢出；管理知识场景切换后显示天枢和灵犀的双语名称与链接。正式站点浏览器复核五款名称正确、无控制台错误。公网返回的 HTML、JS 和两个修改过的 CSS 与本地逐字节一致。发布通过原子替换 `current` 链接完成，未改 Nginx 配置。

## 产品介绍更新验收（2026-10-25）

新增中英文各 15 条能力说明、5 个使用示例，截图改为桌面辅助配图；手机将功能与示例放在截图之前。保持五款应用与两款支撑平台的原有层级，保留全部截图放大、虾说视图切换及语言切换。

在 IAB 中验证 1440/768/390/320 像素中英文无水平溢出；实测截图切换、弹窗 Escape 关闭及双语锚点保留。公网 HTTPS 所有 37 个静态文件与本地逐字节一致，浏览器确认两种语言均显示 15 条能力与 5 个示例。通过原子替换 `current` 完成静态发布，未修改 Nginx 或入口配置；清单位于 `/var/backups/quukk-company/20261025-product-stories/SHA256SUMS`。

## 更新与回滚

双语版本新增 `/en/` 静态目录。Nginx 本站虚拟主机加上 `absolute_redirect off`，保证 `/en` 的补斜线跳转为相对地址 `/en/`，不泄露后端入口的 `:8484` 端口。已验证公网 `/en?ref=homepage` 返回 301、`Location: /en/?ref=homepage`。本次变更前配置及发布清单位于 `/var/backups/quukk-company/20261025-bilingual/`。

正式站点已实测中文 → EN、再次访问根地址恢复英文、英文 → 中文；未出现控制台错误。详细语言行为和响应式检查见项目 README。

将新的 `dist/` 上传到全新的 `releases/<版本>/` 目录，校验内容、目录权限和文件权限后，用临时链接加 `mv -Tf` 原子替换 `current`。相同 root 下更新静态文件不必 reload Nginx。保存旧版本，便于同样方式恢复链接。

若要撤销本次新增虚拟主机，只移除 `/etc/nginx/sites-enabled/zz-quukk-company` 这一条启用链接，执行 `nginx -t`，检查成功后 `systemctl reload nginx`。不要直接覆盖整个 Nginx 备份，以免覆盖其他产品后续配置。站点文件保留供恢复使用。

共享目录 `/var/www/quukk` 服务于其他应用，本次没有改动；官网使用独立 `/var/www/quukk-company`。
