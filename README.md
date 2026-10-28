# ML-Biomat · 杨云浩的研究与开源项目

个人介绍、跨尺度生物材料体系与结构研究、机器学习与多尺度模拟教程。网站：<https://ml-biomat.com/>；个人主页：<https://ml-biomat.com/about/>。

## 修改入口

| 内容 | 源文件 |
| --- | --- |
| 中文个人主页 `/about/` | `content/about-body.html` |
| English profile `/about/en/` | `content/about-en-body.html` |
| 中文简历 `/cv/` | `content/cv-body.html` |
| English CV `/cv/en/` | `content/cv-en-body.html` |
| 分组相册 | `content/profile-albums.json`、`static/images/profile/` |
| FiberNet 展示 | `content/fibernet-body.html` |
| 系列教程与目录 `/tutorials/` | `content/tutorials/polymer-ai/`、`content_tools/tutorials.py` |
| 教程图片、数据与下载 | `static/tutorials/polymer-ai/` |
| 教程样式与筛选 | `static/css/tutorials.css`、`static/js/tutorials.js` |
| 中英文文章 | `content/posts/zh/`、`content/posts/en/` |
| 样式与交互 | `static/css/style.css`、`static/js/main.js`、`static/js/profile.js` |
| 导航、页面模板、生成流程 | `build.py` |
| 站点信息与分类 | `config.py` |

`docs/` 是生成后的发布内容，由构建更新；源文件是日常维护入口。

## 本机使用

Python 3.10 或以上即可构建，核心流程只使用标准库。

```powershell
python manage.py doctor
python manage.py build
python manage.py preview
```

预览地址：<http://127.0.0.1:8866/>。构建默认不联网，预览默认只监听本机。绘图功能 `chart_gen.py` 单独需要 Matplotlib/Pillow。

## 发布

完成修改和预览后，由维护助手执行：

```powershell
python manage.py publish --message "Update personal profile"
```

入口会同步远端状态、构建页面、运行检查、暂存约定的项目文件、提交并推送到 `main`，然后核对远端提交。遇到远端更新、检查失败或异常文件时停止，先完成相应修复；不强制推送。

GitHub Pages 使用仓库生成的站点文件。推送后继续检查仓库部署结果，以及线上页面是否出现这次修改。搜索引擎提交是独立操作，站点上线后需要时执行 `python build.py --submit-indexnow`。

GitHub 登录由本机凭据管理工具保存。仓库地址使用普通 HTTPS URL，凭据和本地私有文件不进入代码仓库。

## 内容与检查

文章保留语言、日期、分类、标签等 frontmatter。`python manage.py check` 检查已生成页面，包含文章/RSS/搜索一致性、站点地图、关键页面和解码后的内部链接。个人经历、论文署名和奖项状态以本人确认资料及原始公开来源为准。

相册默认折叠；照片与论文图保持原比例、完整显示，使用统一相框与留白适配尺寸。图片内容变更后构建会更新资源版本。

## 系列教程维护

高分子与生物大分子教程共20节，中文独立页面位于 `/tutorials/polymer-ai/`。`manifest.json` 维护课名、介绍、阅读分组、主题分类和稳定链接；01–20.html 保留完整讲解、代码、预渲染公式和交互。五组阅读路线同时连接到现有主题分类、站内搜索、RSS与站点地图。当前教程为中文，既有中英文文章继续分别维护。

原始审阅包保持原位。需要重新导入其更新版本时，在装有 Playwright/Chromium 的维护环境运行 `python content_tools/import_polymer_tutorials.py "压缩包路径"`，随后构建与浏览器检查。导入器只转换展示用语、站点路径和样式作用域，不运行科研计算。公式、数据、代码和图片保留原始内容；下载附件分离为独立资源，图片按需加载。

`python manage.py build` 同时验证20节页面、前后节链接、代码入口、站内链接及文章/教程索引完整性。
