[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

# ⠠⠃⠗⠁⠊⠇⠇⠑⠠⠋⠕⠗⠛⠑ BrailleForge

> 離線、零依賴的英語一級點字（非縮寫）工具箱：普通文字 ⇄ Unicode 點字 ⇄ 點位 notation ⇄ Braille ASCII ⇄ 可直接送點字刻印機的 .brf 檔案，五種形態一鍵互轉。

## 🎉 專案介紹

做無障礙內容的人常被同一件事卡住：線上轉換網站能把英文轉成點字圖案，但刻印機和點字顯示器要的卻是 **BRF（Braille ASCII）**，教學材料裡寫的是 **點位（dots-125）**，程式裡存的是 **Unicode 點字圖案**——三種形態互不相通，每轉一次就要換一個網站，還要把內容上傳到別人的伺服器。

BrailleForge 就是為了解決這個斷點而做的**本地優先**工具：全部轉換在本機完成，不連網、不上傳、零第三方依賴，`pip install` 後離線也能用。

**自研差異化亮點**

- 🔁 **五形態互轉閉環**：市面工具大多只做「文字→點字圖案」單向轉換；BrailleForge 打通文字 / Unicode 點字 / 點位 / Braille ASCII / BRF 五種形態，且每條轉換都可逆、有往返測試兜底。
- 🖨️ **真 BRF 排版**：按預設 40 格行寬、25 行/頁生成帶分頁符的 Braille ASCII 檔案，而不是把 Unicode 字元改個副檔名冒充 .brf。
- 🔢 **狀態機而不是查表拼接**：大寫詞（雙大寫符號）、數字模式、數字後接 a–j 字母時的字母符號，都按點字規則用狀態機處理，所以 `NASA`、`2026`、`2a` 這類最容易轉錯的輸入也能正確往返。
- 🌱 **靈感來源**：近期 GitHub Trending 上 local-first / offline-first 專案持續走熱，加上無障礙內容生產裡真實存在的格式斷點——靈感取自這兩個趨勢，程式碼為獨立自研實作，映射依據是公開的點字點位體系與 Braille ASCII 標準表，未複製任何現有專案程式碼。

## ✨ 核心特性

- 🔤 **文字→點字**：英文字母、數字、常用標點的一級（非縮寫）點字編碼，含大寫符號 / 大寫詞 / 數字符號規則
- ↩️ **點字→文字**：狀態機解碼，正確處理數字模式、大寫詞模式與引號歧義格
- 🔡 **Braille ASCII 互轉**：完整實作 64 格標準表（U+2800–U+283F），這是 .brf 檔案的實際位元組編碼
- 🎯 **點位 notation 互轉**：`125-15` 這類教學與校對常用寫法，與點字圖案自由轉換
- 👁️ **點陣檢視**：把每個點字格畫成 ●○ 點陣圖，校對時肉眼可查（對視力校對者友善）
- 📄 **BRF 生成與還原**：可調行寬 / 每頁行數，生成刻印就緒檔案；也能把 .brf 還原回可讀文字
- 📊 **統計報告**：格數、詞數、數字/大寫符號數、按指定版式折算的頁數，JSON 輸出
- 📦 **零依賴**：純 Python 標準庫，Python ≥ 3.9，Windows / macOS / Linux 通用

## 🚀 快速開始

環境要求：Python ≥ 3.9，無其他依賴。

```bash
# 方式一：從原始碼安裝
git clone https://github.com/gitstq/brailleforge.git
cd brailleforge
pip install .

# 方式二：不安裝，直接在原始碼目錄執行
python -m brailleforge demo
```

```bash
brailleforge demo
brailleforge encode "Hello 123"
# ⠠⠓⠑⠇⠇⠕⠀⠼⠁⠃⠉

brailleforge decode "⠠⠓⠑⠇⠇⠕⠀⠼⠁⠃⠉"
# Hello 123
```

## 📖 詳細使用指南

### 命令一覽

| 命令 | 作用 | 範例 |
|---|---|---|
| `encode` | 文字 → Unicode 點字 | `brailleforge encode "Read by touch"` |
| `decode` | Unicode 點字 → 文字 | `brailleforge decode "⠗⠑⠁⠙"` |
| `to-ascii` | Unicode 點字 → Braille ASCII | `brailleforge to-ascii "⠓⠑"` → `HE` |
| `from-ascii` | Braille ASCII → Unicode 點字 | `brailleforge from-ascii ",HI #ABC"` |
| `to-dots` | Unicode 點字 → 點位 | `⠓⠑` → `125-15` |
| `from-dots` | 點位 → Unicode 點字 | `brailleforge from-dots "125-15"` |
| `inspect` | 逐格畫點陣圖 | `brailleforge inspect "⠓"` |
| `brf` | 文字 → 排版好的 .brf | `brailleforge brf -f in.txt -o out.brf --width 40` |
| `unbrf` | .brf → 文字 | `brailleforge unbrf -f out.brf` |
| `stats` | 統計（JSON） | `brailleforge stats "Hello 123"` |

所有命令都支援 `-f 檔案` 讀入、`-o 檔案` 寫出，缺省讀 stdin / 寫 stdout，可自由管線組合。

### 作為 Python 函式庫使用

```python
from brailleforge import encode, decode, format_brf, braille_to_dots

br = encode("Accessibility matters 100")
print(br)                       # ⠠⠁⠉⠉⠑⠎⠎⠊⠃⠊⠇⠊⠞⠽⠀...
print(decode(br))               # Accessibility matters 100
print(braille_to_dots(br))      # 6-1-14-14-15-...
brf_text = format_brf(br, width=40, lines_per_page=25)  # 刻印就緒的 Braille ASCII
```

### 典型場景

- 🏫 **教學材料**：把課文轉成點位 notation 印成練習冊，或用 `inspect` 做課堂演示。
- 🖨️ **送刻印**：`brf` 一步生成符合行寬/分頁的 .brf，交給點字刻印機或轉寫機構，不用再手動折行。
- ✅ **無障礙校對**：拿到一段來歷不明的 BRF，先 `unbrf` 還原成文字核對內容，再動手修改。
- 🤖 **程式整合**：作為函式庫嵌入無障礙內容流水線，全程離線，敏感文字不出本機。

> 📸 演示截圖 / 動圖位置預留：`docs/` 目錄後續補充終端實錄。

## 💡 設計思路與迭代規劃

- **為什麼零依賴純標準庫**：點字轉換是確定性規則，不需要任何重型框架；零依賴意味著十年後這份程式碼大概率還能直接跑。
- **為什麼用狀態機**：點字的大寫、數字都是「模式符號」，脫離上下文無法解碼，查表拼接必然在 `2a`、全大寫詞這類輸入上翻車。
- **誠實標註邊界**：本專案做的是**一級非縮寫**點字；二級縮寫（Grade 2 contractions）規則複雜且有地區差異，未實作前絕不假裝支援。

迭代規劃：

- 🗺️ Grade 2 縮寫支援（可開關，預設關閉）
- 🌏 更多語言體系：法語 / 德語點字映射表
- 🖨️ BRF 元資料校驗器（行寬/分頁合規檢查報告）
- 🔌 MCP / 編輯器外掛形態，方便 AI 代理直接呼叫

## 📦 打包與部署指南

本專案是**工具庫 / CLI 類**專案，按約定不發布平台可執行 Release，整合方式就是安裝即用：

```bash
# 建構發行包（sdist + wheel）
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install build
python -m build        # 產物在 dist/

# 執行測試
python -m unittest discover -s tests -v
```

相容環境：Python ≥ 3.9；Windows / macOS / Linux 均可；無網路、無原生擴充、無環境變數要求。

## 🤝 貢獻指南

- 🐛 Issue：請附最小重現輸入（原文 + 期望點字 + 實際輸出），點字問題最怕「感覺不對」式描述。
- 🔀 PR：提交規範遵循 Angular 風格（`feat:` / `fix:` / `docs:` / `refactor:`），新轉換規則必須附帶往返（round-trip）測試。
- ♿ 特別歡迎點字使用者與轉寫員的回饋：規則對錯，你們說了算。

## 📄 開源協議說明

本專案基於 [MIT License](LICENSE) 開源，可自由使用、修改與分發，保留版權聲明即可。
