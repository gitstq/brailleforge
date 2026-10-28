[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

# ⠠⠃⠗⠁⠊⠇⠇⠑⠠⠋⠕⠗⠛⠑ BrailleForge

> 离线、零依赖的英语一级盲文（非缩写）工具箱：普通文本 ⇄ Unicode 盲文 ⇄ 点位 notation ⇄ Braille ASCII ⇄ 可直接送盲文刻印机的 .brf 文件，五种形态一键互转。

## 🎉 项目介绍

写无障碍内容的人经常被卡在同一件事上：在线转换网站能把英文转成盲文图案，但刻印机和盲文显示器要的却是 **BRF（Braille ASCII）**，教学材料里写的是 **点位（dots-125）**，程序里存的是 **Unicode 盲文图案**——三种形态互不相通，每转一次都要换一个网站，还要把内容上传到别人的服务器。

BrailleForge 就是为解决这个断点而做的**本地优先**工具：全部转换在本机完成，不联网、不上传、零第三方依赖，`pip install` 后断网也能用。

**自研差异化亮点**

- 🔁 **五形态互转闭环**：市面工具大多只做「文本→盲文图案」单向转换；BrailleForge 打通文本 / Unicode 盲文 / 点位 / Braille ASCII / BRF 五种形态，且每条转换都可逆、有往返测试兜底。
- 🖨️ **真 BRF 排版**：按默认 40 格行宽、25 行/页生成带分页符的 Braille ASCII 文件，而不是把 Unicode 字符改个扩展名冒充 .brf。
- 🔢 **状态机而不是查表拼接**：大写词（双大写符号）、数字模式、数字后接 a–j 字母时的字母符号，都按盲文规则用状态机处理，所以 `NASA`、`2026`、`2a` 这类最容易转错的输入也能正确往返。
- 🌱 **灵感来源**：近期 GitHub Trending 上 local-first / offline-first 项目持续走热，加上无障碍内容生产里真实存在的格式断点——灵感取自这两个趋势，代码为独立自研实现，映射依据是公开的盲文点位体系与 Braille ASCII 标准表，未复制任何现有项目代码。

## ✨ 核心特性

- 🔤 **文本→盲文**：英语字母、数字、常用标点的一级（非缩写）盲文编码，含大写符号 / 大写词 / 数字符号规则
- ↩️ **盲文→文本**：状态机解码，正确处理数字模式、大写词模式与引号歧义格
- 🔡 **Braille ASCII 互转**：完整实现 64 格标准表（U+2800–U+283F），这是 .brf 文件的实际字节编码
- 🎯 **点位 notation 互转**：`125-15` 这类教学与校对常用写法，与盲文图案自由转换
- 👁️ **点阵检视**：把每个盲文格画成 ●○ 点阵图，校对时肉眼可查（对视力校对者友好）
- 📄 **BRF 生成与还原**：可调行宽 / 每页行数，生成刻印就绪文件；也能把 .brf 还原回可读文本
- 📊 **统计报告**：格数、词数、数字/大写符号数、按指定版式折算的页数，JSON 输出
- 📦 **零依赖**：纯 Python 标准库，Python ≥ 3.9，Windows / macOS / Linux 通用

## 🚀 快速开始

环境要求：Python ≥ 3.9，无其他依赖。

```bash
# 方式一：从源码安装
git clone https://github.com/gitstq/brailleforge.git
cd brailleforge
pip install .

# 方式二：不安装，直接在源码目录运行
python -m brailleforge demo
```

```bash
brailleforge demo
brailleforge encode "Hello 123"
# ⠠⠓⠑⠇⠇⠕⠀⠼⠁⠃⠉

brailleforge decode "⠠⠓⠑⠇⠇⠕⠀⠼⠁⠃⠉"
# Hello 123
```

## 📖 详细使用指南

### 命令一览

| 命令 | 作用 | 示例 |
|---|---|---|
| `encode` | 文本 → Unicode 盲文 | `brailleforge encode "Read by touch"` |
| `decode` | Unicode 盲文 → 文本 | `brailleforge decode "⠗⠑⠁⠙"` |
| `to-ascii` | Unicode 盲文 → Braille ASCII | `brailleforge to-ascii "⠓⠑"` → `HE` |
| `from-ascii` | Braille ASCII → Unicode 盲文 | `brailleforge from-ascii ",HI #ABC"` |
| `to-dots` | Unicode 盲文 → 点位 | `⠓⠑` → `125-15` |
| `from-dots` | 点位 → Unicode 盲文 | `brailleforge from-dots "125-15"` |
| `inspect` | 逐格画点阵图 | `brailleforge inspect "⠓"` |
| `brf` | 文本 → 排版好的 .brf | `brailleforge brf -f in.txt -o out.brf --width 40` |
| `unbrf` | .brf → 文本 | `brailleforge unbrf -f out.brf` |
| `stats` | 统计（JSON） | `brailleforge stats "Hello 123"` |

所有命令都支持 `-f 文件` 读入、`-o 文件` 写出，缺省读 stdin / 写 stdout，可自由管道组合。

### 作为 Python 库使用

```python
from brailleforge import encode, decode, format_brf, braille_to_dots

br = encode("Accessibility matters 100")
print(br)                       # ⠠⠁⠉⠉⠑⠎⠎⠊⠃⠊⠇⠊⠞⠽⠀...
print(decode(br))               # Accessibility matters 100
print(braille_to_dots(br))      # 6-1-14-14-15-...
brf_text = format_brf(br, width=40, lines_per_page=25)  # 刻印就绪的 Braille ASCII
```

### 典型场景

- 🏫 **教学材料**：把课文转成点位 notation 打印成练习册，或用 `inspect` 做课堂演示。
- 🖨️ **送刻印**：`brf` 一步生成符合行宽/分页的 .brf，交给盲文刻印机或转写机构，不用再手动折行。
- ✅ **无障碍校对**：拿到一段来历不明的 BRF，先 `unbrf` 还原成文本核对内容，再动手修改。
- 🤖 **程序集成**：作为库嵌入无障碍内容流水线，全程离线，敏感文本不出本机。

> 📸 演示截图 / 动图位置预留：`docs/` 目录后续补充终端实录。

## 💡 设计思路与迭代规划

- **为什么零依赖纯标准库**：盲文转换是确定性规则，不需要任何重型框架；零依赖意味着十年后这份代码大概率还能直接跑。
- **为什么用状态机**：盲文的大写、数字都是「模式符号」，脱离上下文无法解码，查表拼接必然在 `2a`、全大写词这类输入上翻车。
- **诚实标注边界**：本项目做的是**一级非缩写**盲文；二级缩写（Grade 2 contractions）规则复杂且有地区差异，未实现前绝不假装支持。

迭代规划：

- 🗺️ Grade 2 缩写支持（可开关，默认关闭）
- 🌏 更多语言体系：法语 / 德语盲文映射表
- 🖨️ BRF 元数据校验器（行宽/分页合规检查报告）
- 🔌 MCP / 编辑器插件形态，方便 AI 代理直接调用

## 📦 打包与部署指南

本项目是**工具库 / CLI 类**项目，按约定不发布平台可执行 Release，集成方式就是安装即用：

```bash
# 构建发行包（sdist + wheel）
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install build
python -m build        # 产物在 dist/

# 运行测试
python -m unittest discover -s tests -v
```

兼容环境：Python ≥ 3.9；Windows / macOS / Linux 均可；无网络、无原生扩展、无环境变量要求。

## 🤝 贡献指南

- 🐛 Issue：请附最小复现输入（原文 + 期望盲文 + 实际输出），盲文问题最怕「感觉不对」式描述。
- 🔀 PR：提交规范遵循 Angular 风格（`feat:` / `fix:` / `docs:` / `refactor:`），新转换规则必须附带往返（round-trip）测试。
- ♿ 特别欢迎盲文使用者与转写员的反馈：规则对错，你们说了算。

## 📄 开源协议说明

本项目基于 [MIT License](LICENSE) 开源，可自由使用、修改与分发，保留版权声明即可。
