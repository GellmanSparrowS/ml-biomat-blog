# ML-Biomat · 杨云浩的研究与开源项目

个人介绍、纤维生物材料研究、机器学习与多尺度模拟教程。网站：<https://ml-biomat.com/>；个人主页：<https://ml-biomat.com/about/>。

## 修改入口

| 内容 | 源文件 |
| --- | --- |
| 个人主页 | `content/about-body.html` |
| 完整简历 | `content/cv-body.html` |
| FiberNet 展示 | `content/fibernet-body.html` |
| 中英文文章 | `content/posts/zh/`、`content/posts/en/` |
| 样式与交互 | `static/css/style.css`、`static/js/main.js` |
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
