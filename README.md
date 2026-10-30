# ML-Biomat · 杨云浩的研究与开源项目

个人介绍、跨尺度生物材料体系与结构研究、机器学习与多尺度模拟教程。网站：<https://ml-biomat.com/>；个人主页：<https://ml-biomat.com/about/>。

## 修改入口

| 内容 | 源文件 |
| --- | --- |
| 中文个人主页 `/about/` | `content/about-body.html` |
| English profile `/about/en/` | `content/about-en-body.html` |
| 中文简历 `/cv/` | `content/cv-body.html` |
| English CV `/cv/en/` | `content/cv-en-body.html` |
| 相册素材与来源 | `content/profile-albums.json`、`static/images/profile/` |
| 活动展示 | `content/about-body.html`、`content/about-en-body.html`；首页共用其中的活动条目 |
| FiberNet 中英文展示 | `content/fibernet-body.html`、`content/fibernet-en-body.html`、`static/css/fibernet.css` |
| 分类与教程 | `content_tools/catalog.py`、`content/tutorials/polymer-ai/`、`content_tools/tutorials.py` |
| 教程图片、数据与下载 | `static/tutorials/polymer-ai/` |
| 教程样式 | `static/css/tutorials.css` |
| 中英文文章 | `content/posts/zh/`、`content/posts/en/` |
| 全站布局与交互 | `static/css/style.css`、`static/css/site-layout.css`、`static/css/site-refinement.css`、`static/js/main.js`、`static/js/site-catalog.js` |
| 个人页与活动图库 | `static/css/profile-layout.css`、`static/js/profile-gallery.js` |
| 公共导航与主题初始化 | `content_tools/chrome.py`、`static/js/main.js` |
| 中英首页、分类与文章合集 | `content_tools/home.py`、`content_tools/catalog.py`、`content_tools/site_layouts.py` |
| 中英工具、隐私与标签页 | `content_tools/utility_pages.py`、`content_tools/tag_pages.py` |
| 页面模板与生成流程 | `build.py` |
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

## 分类与图文教程维护

20篇高分子与生物大分子图文教程按主题融入 `/categories/`，与既有文章使用同一分类列表，不再展示独立系列。中文分类位于 `/categories/` 和 `/categories/{topic}/`，英文对应 `/categories/en/` 和 `/categories/{topic}/en/`。旧教程正文地址保持有效，旧目录 `/tutorials/` 与 `/tutorials/polymer-ai/` 自动进入分类。`manifest.json` 维护标题、介绍、主题及稳定地址；01–20.html 保留完整讲解、代码、预渲染公式和交互。

原始审阅包保持原位。需要重新导入其更新版本时，在装有 Playwright/Chromium 的维护环境运行 `python content_tools/import_polymer_tutorials.py "压缩包路径"`，随后构建与浏览器检查。导入器只转换展示用语、站点路径和样式作用域，不运行科研计算。公式、数据、代码和图片保留原始内容；下载附件分离为独立资源，图片按需加载。

`python manage.py build` 同时验证20篇教程的分类入口、代码与附件、48篇既有文章的双语互链和标题、图文覆盖及全站链接。手机目录默认折叠；正文和间距紧凑呈现，原图保持比例并可放大。

既有文章新增的双语讲解图保存在 `static/images/article-guides/`，可通过 `content_tools/illustrate_mechanics.py` 和 `content_tools/illustrate_computing.py` 复现。教学曲线的生成参数与示意性质在脚本和图注中记录。


## 全站语言与主题

中文首页为 `/`，英文首页为 `/en/`；旧 `/zh/` 显示中文首页。完整内容合集独立在 `/articles/` 与 `/articles/en/`，语言开关只切换同一类页面。中文顶栏为“首页、工具库、分类、个人主页”，英文为“Home、Library、Categories、Profile”，所有页面保持同一套按钮结构和栏目高亮。

默认主题在样式加载前设为暗色；访客手动选择亮色后，跨页和刷新保留。语言由明确URL决定，普通导航和Logo保持当前语言。没有英文译文的20篇教程仍保留EN控件的位置，以禁用状态呈现，不跳转到无关列表。

每篇内容只有一个主分类，其余方法与材料信息用标签表达。中文与英文的主分类按实际收录内容独立计数。`qa_check.py`同时检查各页公共导航、默认主题和首页成对关系；浏览器验收须使用空存储的新会话覆盖系统浅色和深色，实际点击主题及完整导航流程。

## 已确认的研究主页布局

首页与个人页共用活动内容和图库：首页为横向概览，个人页为完整纵向时间线。活动照片与题名直接打开相册；论文题名使用已确认的期刊链接。个人页保留横向合作项目，近期论文及荣誉标题位于内容上方。研究主线使用用户确认文字，不插入强制换行。

布局通过正式源文件维护，`python manage.py build` 会同时生成首页、分类、文章合集和中英文个人页；无须依赖 `.local/` 下的历史预览生成器。


## 生物与高分子材料图文教程（2026-10-29）

新增48篇双语教程，在既有分类中按正文主题分为材料与结构23篇、物理建模与模拟21篇、实验表征与数据分析4篇。中文与英文各有48个独立页面，保留完整讲解、395个公式、228幅图和56个教学交互（每种语言）。全站分类共92篇中文、72篇英文，统一接入搜索、RSS和站点地图。

源码为 `content/tutorials/biomaterials-courses/`，其中 `manifest.json` 记录双语题名、目录、分类及原文摘要校验。`content_tools/biomaterials_courses.py` 生成共享导航页面；`content_tools/import_biomaterials_courses.py` 从原课程文件夹导入正文和实验脚本，保留源文件。页面样式与图示浏览分别为 `static/css/biomaterials-courses.css` 和 `static/js/biomaterials-courses.js`。稳定路由例如 `/tutorials/biomaterials-courses/cp09/` 与 `/tutorials/biomaterials-courses/cp09/en/`，语言切换保持对应章节。

## 首页与网络动态

首页继续显示自动旋转的三维纤维网络，使用 `static/js/fibernet-scene.js`。全站背景在手机上限帧运行，低功耗及慢帧设备进一步降低帧率；返回页面恢复动画，默认自动播放。

FiberNet 首屏使用 `static/js/fibernet-flow.js` 与 `static/data/fibernet-flow.json`。这是种子固定的标量弹簧网络传力与键逾渗示意：330个节点、989条边和31个连通状态，颜色由各状态平衡后的归一化边载荷产生。它与项目展示的FEM计算图例分别维护。`content_tools/generate_fibernet_flow.py` 可用NumPy/SciPy重新生成数据，日常网站构建直接使用已提交数据，不增加构建依赖。动画不设操作控件，画布按设备像素密度绘制。


## 动态设置与轻量图片（2026-10-30）

本站默认自动播放，首次访问或普通刷新均无需启用链接。可选的`?motion=off`暂停、`?motion=auto`跟随系统、`?motion=on`恢复播放都会记住本设备的明确选择，刷新、切换语言和进入其他页面继续生效。清除选择后恢复默认播放。FiberNet图形宽高为最初版本的70%，节点、连线与运动节奏保留。处理后地址自动恢复正常页面路径。共享策略为 `static/js/site-motion.js`，Canvas及CSS过渡使用同一设置；不修改系统设置。验证真实Edge时用Playwright `reduced_motion='null'`，否则默认测试环境会替换系统偏好。

`content_tools/image_delivery.py`只改生成HTML中的图片标签：中等清晰度预览、响应式宽度、图片尺寸、延迟加载与原图地址。`static/images/previews/manifest.json`封存原图和预览的尺寸及SHA；原图保持原位，科学SVG和公式继续使用矢量。相册和通用图示查看器先显示预览，高清图加载解码后替换。`content_tools/generate_image_previews.py`重新生成预览时需要Pillow，常规网站构建继续只用标准库。

代码高亮使用 `static/js/code-highlight.js` 按需加载 `static/vendor/highlightjs/11.11.1/` 中的固定版本，许可与源地址保存在同目录。页面没有代码时无需加载高亮库；动画启动不等待高亮资源。背景和三维画布复用未变尺寸的背板与数据，滚动更新合并到动画帧，搜索请求合并复用。
