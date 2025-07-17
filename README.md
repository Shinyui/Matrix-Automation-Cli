# 📱 Instageam 自動化腳本

一個用 Python 撰寫的 Instagram 自動化工具，可透過 ADB 操作多台 Android 裝置，模擬滑動、點讚、留言等行為，支援裝置掃描與批次模擬執行

## 🚀 功能特色

- 🔍 掃描目前透過 ADB 連接的 Android 裝置，並輸出為 CSV
- 🤖 載入裝置清單後，平行執行模擬操作流程
- 🧠 支援狀態機與轉移機率配置，擴充彈性強
- ✅ 模組化設計，方便擴展與測試

## 🧩 專案結構

```
ins_automation/
├── cli.py                        # CLI 入口點，定義 scan/simulate 指令
├── ins_automation/
│   ├── actions.py               # 各種操作：滑動、點讚、進入留言等
│   ├── devices.py               # 裝置連接與 CSV 匯入/輸出
│   ├── runner.py                # 多裝置模擬控制器
│   ├── states.py                # 定義狀態與轉移矩陣
│   ├── walk.py                  # 實作帶有轉移機率的隨機狀態機
```

## 🛠️ 安裝方式

1. 安裝 Python 3.8+
2. 安裝依賴：

```bash
pip install -r requirements.txt
```

> 📦 若未提供 requirements.txt，請確保手動安裝 `uiautomator2`

3. 確認已安裝 ADB 並加入環境變數：

```bash
adb devices
```

## 🖥️ 使用方式

### 🔍 掃描裝置並輸出為 CSV

```bash
python cli.py scan --path /path/to/adb --output devices.csv
```

- `--path`：**指定 ADB 可執行檔的路徑，例如 `/opt/homebrew/bin/adb` 或 `C:\platform-tools\adb.exe`
- `--output`：輸出裝置資訊的 CSV 檔名，預設為 `devices.csv`

✅ 範例（使用 macOS + brew 安裝的 adb）：

```bash
python cli.py scan --path /opt/homebrew/bin/adb --output devices.csv
```

### 🤖 執行首頁養號操作

```bash
python cli.py simhome --csv devices.csv --steps 100
```

將針對 CSV 中列出的每台裝置，啟動一段預設的模擬互動流程。

## 📝 注意事項

- 須使用 Android 實體裝置並開啟「USB 偵錯」
- 若模擬過於頻繁，可能導致帳號風險，請斟酌使用
